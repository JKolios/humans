import actions


class CharacterClass(object):
    actions_owned_by_class = []

    @classmethod
    def instantiate_actions(cls):
        return [init_tuple[0](init_tuple[1]) for init_tuple in cls.actions_owned_by_class]


class Devastator(CharacterClass):
    max_hp = 80
    actions_owned_by_class = [(actions.Banhammer, {})]


class Human(CharacterClass):

    max_hp = 50
    actions_owned_by_class = [(actions.Fists, {})]


class Thief(Human):
    actions_owned_by_class += [(actions.PoisonedDagger, {})]
    armor = 1


class Warrior(Human):
    actions_owned_by_class += [(actions.Broadsword, {})]
    armor = 2


class Mage(Human):

    actions_owned_by_class += [(actions.Fireball, {})]
    armor = 0


class Priest(Human):

    actions_owned_by_class += [(actions.RayOfFrost, {}), (actions.MinorHeal, {})]
    armor = 0


class Brigand(Human):

    actions_owned_by_class += [(actions.SerratedCleaver, {})]
    armor = 1


class Grenadier(Human):

    actions_owned_by_class += [(actions.PitchVial, {}), (actions.PitchVial, {}), (actions.PitchVial, {})]
    armor = 0
