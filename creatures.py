from random import choice

import attacks
import statuses


DEFAULT_MAX_HP = 100

status_string = """%s\nCLASS: %s\nHP: %s\nSTATUSES: %s """


class Creature(object):

    def __init__(self, name):
        self.name = name

        self.set_max_hp(DEFAULT_MAX_HP)

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
        elif actual_delta == 0 and hp_delta > 0 :
            print "There was no effect!"
        if self.hp <= 0:
            statuses.Death().apply_to_actor(self)
            raise Death(self)

    def attack(self, target=None, available_targets=None, attack_used=None):
        if not target and not available_targets:
            raise InvalidAttackCall

        if not attack_used:
            attack_used = self._select_attack()

        if attack_used not in self.attacks:
            raise InvalidAttackUsed

        if not target:
            target = self._select_target(available_targets, attack_used)

        if not hasattr(target, 'receive_attack') and callable(getattr(target, 'receive_attack')):
            raise InvalidAttackTarget
        # TODO: Introduce attacks hitting or missing based on accuracy

        print attack_used.attack_message(self.name, target.name)
        target.receive_attack(attack_used)

    def _select_target(self, available_targets, attack):
            # TODO: Target selection logic?
            if attack.is_heal:
                return self
            return choice(available_targets)

    def _select_attack(self):
        # TODO: Attack selection logic? Probably based on target
        if self._low_hp():
            heals_available = [attack for attack in self.attacks if attack.is_heal]
            if heals_available:
                return choice(heals_available)

        return choice(self.attacks)

    def _low_hp(self):
        return self.hp <= self.max_hp * 0.2

    def receive_attack(self, attack):
        try:
            if hasattr(attack, 'damage'):
                for damage_type, damage_magnitude in attack.damage.iteritems():
                    # physical damage is calculated separately because it's intended to have other mechanics in the future
                    # TODO: specify other mechanics
                    if damage_type == 'physical':
                        self.modify_hp(-(damage_magnitude - self.armor))
                    # resolve all other types of damage against the target's resistance with the same name
                    else:
                        self.modify_hp(-(damage_magnitude - self.resistances.get(damage_type, 0)))

            if hasattr(attack, 'applies_statuses'):
                for status in attack.applies_statuses:
                    new_status = statuses.make(status[0], status[1])
                    new_status.apply_to_actor(self)

        except Death as e:
            raise e


class Devastator(Creature):
    def __init__(self, name):
        Creature.__init__(self, name)
        self.set_max_hp(80)
        self.attacks = [attacks.Banhammer]


class Human(Creature):
    def __init__(self, name):
        Creature.__init__(self, name)
        self.set_max_hp(80)
        self.attacks = [attacks.Fists]


class Thief(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks += [attacks.PoisonedDagger]
        self.armor = 1


class Warrior(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks += [attacks.Broadsword]
        self.armor = 2


class Mage(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks += [attacks.Fireball]
        self.armor = 0


class Priest(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks += [attacks.RayOfFrost, attacks.MinorHeal]
        self.armor = 0


class Brigand(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.attacks += [attacks.SerratedCleaver]
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