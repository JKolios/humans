from random import choice

from attacks import *
import statuses


DEFAULT_MAX_HP = 100

status_string = """%s\nCLASS: %s\nHP: %s\nSTATUSES: %s """


class Creature(object):
    attacks_owned_by_class = []

    def __init__(self, name):
        self.name = name

        self.max_hp = DEFAULT_MAX_HP
        self.hp = self.max_hp

        self.statuses = []
        self.regen_per_turn = 1

        self.armor = 0
        self.resistances = {
            'energy': 0,
            'frost': 0,
            'fire': 0,
            'shock': 0
        }

        self.attacks = []

        self.can_act = True

    def __repr__(self):
        if statuses.Death in self.statuses:
            return '%s\nCLASS: %s\n-DEAD-' % (self.name, self.__class__.__name__)
        else:
            return status_string % (
                self.name, self.__class__.__name__,
                self.hp,
                [status.name for status in self.statuses])

    def _instantiate_attacks(self):
        for init_tuple in self.attacks_owned_by_class:
            self.attacks.append(attack_factory(init_tuple[0], init_tuple[1]))

    def set_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.hp = self.max_hp

    def process_statuses(self):
        try:
            for status in self.statuses:
                status.apply_effect_and_check_duration()
            if len(self.statuses) == 0 and self.hp < self.max_hp:
                self.modify_hp(self.regen_per_turn)

        except Death as e:
            raise e

    def modify_hp(self, hp_delta):
        actual_delta = min(hp_delta, self.max_hp - self.hp)
        self.hp += actual_delta
        if actual_delta > 0:
            print "%s gained %s HP!" % (self.name, abs(hp_delta))
        elif actual_delta < 0:
            print "%s lost %s HP!" % (self.name, abs(hp_delta))
        elif actual_delta == 0 and hp_delta > 0:
            print "There was no effect!"
        if self.hp <= 0:
            statuses.Death().apply_to_actor(self)
            raise Death(self)

    def attack(self, target=None, available_targets=None, attack_used=None):
        if not target and not available_targets:
            raise InvalidAttackCall

        # attack selection phase
        if not attack_used:
            attack_used = self._select_attack()

        if attack_used not in self.attacks:
            raise InvalidAttackUsed

        # target selection phase
        if not target:
            target = self._select_target(available_targets, attack_used)

        if not hasattr(target, 'receive_attack') or not callable(getattr(target, 'receive_attack')):
            raise InvalidAttackTarget
        # TODO: Introduce attacks hitting or missing based on accuracy

        # cooldown application
        attack_used.use()

        print attack_used.attack_message(self.name, target.name)
        target.receive_attack(attack_used)

    def _select_target(self, available_targets, attack):
        # TODO: Target selection logic?
        if attack.is_heal:
            return self
        return choice(available_targets)

    def _select_attack(self):
        # TODO: Attack selection logic? Probably based on target
        # TODO: Improve naive attack selection logic vis. cooldowns
        attacks_available = [attack for attack in self.attacks if attack.is_available()]
        if self._low_hp():
            heals_available = [attack for attack in attacks_available if attack.is_heal]
            if heals_available:
                return choice(heals_available)
        return choice(attacks_available)

    def _low_hp(self):
        return self.hp <= self.max_hp * 0.2

    def receive_attack(self, attack):
        try:
            if hasattr(attack, 'damage'):
                for damage_type, damage_magnitude in attack.damage.iteritems():
                    # physical damage is calculated separately because it's intended to have other mechanics in the future
                    # TODO: specify other mechanics
                    if damage_type == 'physical':
                        self.modify_hp(-(max(damage_magnitude - self.armor, 0)))
                    # resolve all other types of damage against the target's resistance with the same name
                    else:
                        self.modify_hp(-(max(damage_magnitude - self.resistances.get(damage_type, 0), 0)))

            if hasattr(attack, 'applies_statuses'):
                for status in attack.applies_statuses:
                    new_status = statuses.status_factory(status[0], status[1])
                    new_status.apply_to_actor(self)

        except Death as e:
            raise e

    def process_cooldowns(self):
        for attack in self.attacks:
            attack.process_cooldown()


class Devastator(Creature):
    def __init__(self, name):
        Creature.__init__(self, name)
        self.set_max_hp(80)
        self.attacks_available_to_class_to_class = [(Banhammer, {})]
        self._instantiate_attacks()


class Human(Creature):
    def __init__(self, name):
        Creature.__init__(self, name)
        self.set_max_hp(80)
        self.attacks_owned_by_class = [(Fists, {})]


class Thief(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks_owned_by_class += [(PoisonedDagger, {})]
        self._instantiate_attacks()
        self.armor = 1


class Warrior(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks_owned_by_class += [(Broadsword, {})]
        self._instantiate_attacks()
        self.armor = 2


class Mage(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks_owned_by_class += [(Fireball, {})]
        self._instantiate_attacks()
        self.armor = 0


class Priest(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks_owned_by_class += [(RayOfFrost, {}), (MinorHeal, {})]
        self._instantiate_attacks()
        self.armor = 0


class Brigand(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks_owned_by_class += [(SerratedCleaver, {})]
        self._instantiate_attacks()
        self.armor = 1


class InvalidAttackCall(Exception):
    pass


class InvalidAttackUsed(Exception):
    pass


class InvalidAttackTarget(Exception):
    pass


class Death(Exception):
    def __init__(self, dead_creature):
        super(Death, self).__init__()
        self.dead_creature = dead_creature