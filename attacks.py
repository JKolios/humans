import statuses
VALID_ATTACK_TYPES = ['physical', 'magical']

# TODO: Per-attack cooldown logic?


class Attack(object):
    name = 'Generic Attack'
    is_heal = False
    cooldown_per_use = 0
    attack_description = '%s attacks %s using the abstract notion of attacking! You broke something!'

    def __init__(self, kwargs):
        # kwargs may be used in the future to supply instance init data
        self.cooldown = 0
        self.times_used = 0

    def use(self):
        # the +1 accounts for the current turn
        self.cooldown += self.cooldown_per_use + 1
        self.times_used += 1

    def is_available(self):
        return self.cooldown == 0

    def process_cooldown(self):
        self.cooldown = max(self.cooldown-1, 0)


    @classmethod
    def attack_message(cls, user, target):
        if cls.attack_description.count('%s') == 1:
            return cls.attack_description % user
        elif cls.attack_description.count('%s') == 2:
            return cls.attack_description % (user, target)
        elif cls.attack_description.count('%s') == 3:
            return cls.attack_description % (user, target, cls.name)
        else:
            return 'Something indescribable happens!'


class Fists(Attack):
    name = 'Fists'
    damage = {'physical': 2}
    accuracy = 0.8
    attack_description = '%s punches %s!'


class Broadsword(Attack):
    name = 'Broadsword'
    damage = {'physical': 10}
    accuracy = 0.75
    attack_description = '%s swings at %s with a %s!'


class PoisonedDagger(Attack):
    name = 'Poisoned Dagger'
    damage = {'physical': 5}
    applies_statuses = [(statuses.Poison, {'duration': 4, 'intensity': 4})]
    accuracy = 0.75
    attack_description = '%s stabs %s with a %s!'


class SerratedCleaver(Attack):
    name = 'Serrated Cleaver'
    damage = {'physical': 8}
    applies_statuses = [(statuses.Bleeding, {'duration': 5})]
    accuracy = 0.8
    attack_description = '%s swings at %s with a %s! Blood pours from the wound!'


class Fireball(Attack):
    name = 'Fireball'
    damage = {'fire': 15}
    cooldown_per_use = 1
    accuracy = 0.6
    attack_description = '%s throws a fireball at %s!'


class MinorHeal(Attack):
    name = 'Minor Heal'
    accuracy = 1
    is_heal = True
    applies_statuses = [(statuses.Healing, {'duration': 1, 'intensity': 10})]
    cooldown_per_use = 2
    attack_description = '%s uses Minor Heal!'


class RayOfFrost(Attack):
    name = 'Ray of Frost'
    damage = {'frost': 3}
    applies_statuses = [(statuses.Frozen, {'duration': 2})]
    accuracy = 0.6
    cooldown_per_use = 2
    attack_description = '%s casts a Ray of Frost on %s!'


class Banhammer(Attack):
    name = 'Banhammer'
    damage = {'energy': 150}
    accuracy = 1.0
    magical_damage = 150
    cooldown_per_use = 1
    attack_description = '%s erases %s from existance!'


def attack_factory(status_class, kwargs):
    if not Attack.__subclasscheck__(status_class):
        raise InvalidFactoryArgument
    return status_class(kwargs)


class InvalidFactoryArgument(Exception):
    pass

