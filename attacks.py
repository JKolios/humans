import statuses
VALID_ATTACK_TYPES = ['physical', 'magical']


class Attack(object):
    name = 'Generic Attack'
    types = ['physical']


class Fists(Attack):
    name = 'Fists'
    types = ['physical']
    physical_damage = 2
    accuracy = 0.8


class Broadsword(Attack):
    name = 'Broadsword'
    types = ['physical']
    physical_damage = 10
    accuracy = 0.75


class PoisonedDagger(Attack):
    name = 'Poisoned Dagger'
    types = ['physical']
    applies_statuses = [statuses.Poison(4, 4)]
    accuracy = 0.75
    physical_damage = 5


class Fireball(Attack):
    name = 'Fireball'
    types = ['magical']
    accuracy = 0.6
    magical_damage = 15


class RayOfFrost(Attack):
    name = 'Ray of Frost'
    types = ['magical']
    applies_statuses = [statuses.Frozen(2)]
    accuracy = 0.6
    magical_damage = 3


class Banhammer(Attack):
    name = 'Banhammer'
    types = ['magical']
    accuracy = 1.0
    magical_damage = 150
