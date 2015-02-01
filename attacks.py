import statuses
VALID_ATTACK_TYPES = ['physical', 'magical']

# TODO: Per-attack cooldown logic?


class Attack(object):
    name = 'Generic Attack'
    is_heal = False
    cooldown_per_use = 0
    accuracy = 1.0
    attempt_description = '%s attacks %s using the abstract notion of attacking! You broke something!'
    success_description = '%s succeeded using the abstract notion of attacking! You broke something harder!'

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
    def attempt_message(cls, user, target):
        if cls.attempt_description.count('%s') == 1:
            return cls.attempt_description % user
        elif cls.attempt_description.count('%s') == 2:
            return cls.attempt_description % (user, target)
        elif cls.attempt_description.count('%s') == 3:
            return cls.attempt_description % (user, target, cls.name)
        else:
            return 'Something indescribable happens!'

    @classmethod
    def success_message(cls, target):
        if cls.success_description.count('%s') == 0:
            return cls.success_description
        elif cls.success_description.count('%s') == 1:
            return cls.success_description % target
        elif cls.success_description.count('%s') == 2:
            return cls.success_description % (cls.name, target)
        else:
            return 'Something indescribable happens!'


class Fists(Attack):
    name = 'Fists'
    damage = {'physical': 2}
    accuracy = 0.8
    attempt_description = '%s punches %s!'
    success_description = 'The punch connects!'


class Broadsword(Attack):
    name = 'Broadsword'
    damage = {'physical': 10}
    accuracy = 0.75
    attempt_description = '%s swings at %s with a %s!'
    success_description = 'The %s slices through %s\'s flesh!'


class PoisonedDagger(Attack):
    name = 'Poisoned Dagger'
    damage = {'physical': 5}
    applies_statuses = [(statuses.Poison, {'duration': 4, 'intensity': 4})]
    accuracy = 0.75
    attempt_description = '%s stabs at %s with a %s!'
    success_description = 'The %s digs deep through %s\'s body, releasing poison!'


class SerratedCleaver(Attack):
    name = 'Serrated Cleaver'
    damage = {'physical': 8}
    applies_statuses = [(statuses.Bleeding, {'duration': 5})]
    accuracy = 0.8
    attempt_description = '%s swings at %s with a %s!'
    success_description = 'The %s mangles %s\'s flesh! Blood pours from the wound!'


class Fireball(Attack):
    name = 'Fireball'
    damage = {'fire': 15}
    cooldown_per_use = 1
    accuracy = 0.6
    attempt_description = '%s throws a fireball at %s!'
    success_description = 'The fireball hits with a tremendous explosion!'


class MinorHeal(Attack):
    name = 'Minor Heal'
    accuracy = 1
    is_heal = True
    applies_statuses = [(statuses.Healing, {'duration': 1, 'intensity': 10})]
    cooldown_per_use = 2
    attempt_description = '%s uses Minor Heal!'
    success_description = '%s\'s wounds start to close!'


class RayOfFrost(Attack):
    name = 'Ray of Frost'
    damage = {'frost': 3}
    applies_statuses = [(statuses.Frozen, {'duration': 2})]
    accuracy = 0.6
    cooldown_per_use = 2
    attempt_description = '%s casts a Ray of Frost on %s!'
    success_description = 'The ray finds its target. The air around %s instantly freezes!'


class Banhammer(Attack):
    name = 'Banhammer'
    damage = {'energy': 150}
    accuracy = 0.6
    cooldown_per_use = 1
    attempt_description = '%s swings the Banhammer at %s!'
    success_description = 'No trace of %s\'s existence remains in this world!'


def attack_factory(status_class, kwargs):
    if not Attack.__subclasscheck__(status_class):
        raise InvalidFactoryArgument
    return status_class(kwargs)


class InvalidFactoryArgument(Exception):
    pass

