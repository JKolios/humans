from random import choice, random

import actions
import effects
import metaclasses
import collections

from actions.exceptions import InvalidActionCall, InvalidActionUsed, InvalidActionTarget

DEFAULT_MAX_HP = 100

status_string_living = '%s\nCLASS: %s\nHP: %s\nSTATUSES: %s\n'
status_string_dead = '%s\nCLASS: %s\n-DEAD-\n'


class Actor(object, metaclass=metaclasses.RegisterLeafClasses):
    actions_owned_by_class = []

    def __init__(self, name):
        self.name = name

        self.max_hp = DEFAULT_MAX_HP
        self.hp = self.max_hp

        self.effects = []
        self.regen_per_turn = 1

        self.armor = 0
        self.resistances = {
            'energy': 0,
            'frost': 0,
            'fire': 0,
            'shock': 0
        }

        self.actions = []

        self.can_act = True

    def __repr__(self):
        if effects.Death in self.effects:
            return status_string_dead % (self.name, self.__class__.__name__)
        else:
            return status_string_living % (
                self.name, self.__class__.__name__,
                self.hp,
                [status.name for status in self.effects])

    def _instantiate_actions(self):
        for init_tuple in self.actions_owned_by_class:
            self.actions.append(actions.action_factory(init_tuple[0], init_tuple[1]))

    def set_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.hp = self.max_hp

    def process_effects(self):
        try:
            for status in self.effects:
                status.apply_effect_and_check_duration()
            if len(self.effects) == 0 and self.hp < self.max_hp:
                self.modify_hp(self.regen_per_turn)

        except Death as e:
            raise e

    def modify_hp(self, hp_delta):
        actual_delta = min(hp_delta, self.max_hp - self.hp)
        self.hp += actual_delta
        if actual_delta > 0:
            print("%s gained %s HP!" % (self.name, abs(hp_delta)))
        elif actual_delta < 0:
            print("%s lost %s HP!" % (self.name, abs(hp_delta)))
        elif actual_delta == 0 and hp_delta > 0:
            print("There was no effect!")
        if self.hp <= 0:
            effects.Death().apply_to_actor(self)
            raise Death(self)

    def take_action(self, target=None, available_targets=None, action_used=None):
        if not target and not available_targets:
            raise InvalidActionCall

        # action selection phase
        if not action_used:
            action_used = self._select_action()
            if action_used is None:
                return

        if action_used not in self.actions:
            raise InvalidActionUsed

        # target selection phase
        if not target:
            target = self._select_target(available_targets, action_used)

        if not hasattr(target, 'receive_action') \
                or not isinstance(getattr(target, 'receive_action'), collections.Callable):
            raise InvalidActionTarget

        # cooldown application
        action_used.use()

        print(action_used.generate_message('attempt', self.name, target.name))
        target.receive_action(action_used)

    def _select_target(self, available_targets, action):
        # TODO: Target selection logic?
        if action.is_heal:
            return self
        return choice(available_targets)

    def _select_action(self):
        # TODO: Better Action selection logic? Probably based on target
        # TODO: Improve naive action selection logic vis. cooldowns

        actions_available = [action for action in self.actions if action.is_available()]
        if len(actions_available) == 0:
            return None

        # Action selection logic, in order:

        # If low on HP, try to use a heal
        if self._low_hp():
            heals_available = [action for action in actions_available if isinstance(action, actions.Heal)]
            if heals_available:
                print(heals_available[0].total_heal)
                return sorted(heals_available, key=lambda heal: heal.total_heal, reverse=True)[0]

        # If you have something that inflicts a (negative) status, use it
        attacks_with_effects = [action for action in actions_available
                                if isinstance(action, actions.Attack) and action.applies_effects]
        if attacks_with_effects:
            return choice(attacks_with_effects)

        # Pick the action with the highest sum of all damage types
        actions_available.sort(key=lambda act: act.total_damage, reverse=True)
        return actions_available[0]

    def _low_hp(self):
        return self.hp <= self.max_hp * 0.2

    def receive_action(self, action_received):
        try:
            # Resolve whether the action hit
            action_roll = random()
            if action_roll <= (1.0 - action_received.accuracy):
                print(action_received.generate_message('failure', self.name))
                return
            else:
                print(action_received.generate_message('success', self.name))

            # Resolve damage reduction
            if hasattr(action_received, 'damage'):
                for damage_type, damage_magnitude in action_received.damage.items():
                    # physical damage is calculated separately because it's intended to have other mechanics eventually
                    # TODO: specify other mechanics
                    if damage_type == 'physical':
                        self.modify_hp(-(max(damage_magnitude - self.armor, 0)))
                    # resolve all other types of damage against the target's resistance with the same name
                    else:
                        self.modify_hp(-(max(damage_magnitude - self.resistances.get(damage_type, 0), 0)))

            # resolve any effects the action may apply
            if hasattr(action_received, 'applies_effects'):
                for status in action_received.applies_effects:
                    new_status = effects.status_factory(status[0], status[1])
                    new_status.apply_to_actor(self)

        except Death as e:
            raise e

    def process_cooldowns(self):
        for action in self.actions:
            action.process_cooldown()


class Devastator(Actor):
    def __init__(self, name):
        Actor.__init__(self, name)
        self.set_max_hp(80)
        self.actions_owned_by_class = [(actions.Banhammer, {})]
        self._instantiate_actions()


class Human(Actor):
    def __init__(self, name):
        Actor.__init__(self, name)
        self.set_max_hp(50)
        self.actions_owned_by_class = [(actions.Fists, {})]


class Thief(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.actions_owned_by_class += [(actions.PoisonedDagger, {})]
        self._instantiate_actions()
        self.armor = 1


class Warrior(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.actions_owned_by_class += [(actions.Broadsword, {})]
        self._instantiate_actions()
        self.armor = 2


class Mage(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.actions_owned_by_class += [(actions.Fireball, {})]
        self._instantiate_actions()
        self.armor = 0


class Priest(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.actions_owned_by_class += [(actions.RayOfFrost, {}), (actions.MinorHeal, {})]
        self._instantiate_actions()
        self.armor = 0


class Brigand(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.actions_owned_by_class += [(actions.SerratedCleaver, {})]
        self._instantiate_actions()
        self.armor = 1


class Grenadier(Human):
    def __init__(self, name):
        Human.__init__(self, name)
        self.actions_owned_by_class += [(actions.PitchVial, {}), (actions.PitchVial, {}), (actions.PitchVial, {})]
        self._instantiate_actions()
        self.armor = 0


class Death(Exception):
    def __init__(self, dead_creature):
        super(Death, self).__init__()
        self.dead_creature = dead_creature
