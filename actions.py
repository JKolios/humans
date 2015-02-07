import statuses

INFINITE = -1

class Action(object):
    name = 'Generic Action'
    is_heal = False
    cooldown_per_use = 0
    available_uses = INFINITE
    damage = {}
    accuracy = 1.0
    applies_statuses = []
    descriptions = {
        'attempt': 'Attempt Placeholder!',
        'success': 'Success Placeholder!',
        'failure': 'Failure Placeholder!'
    }

    def __init__(self, kwargs):
        # kwargs may be used in the future to supply instance init data
        self.cooldown = 0
        self.times_used = 0

    def use(self):
        # the +1 accounts for the current turn
        self.cooldown += self.cooldown_per_use + 1
        self.available_uses = min(self.available_uses - 1, 0)

    def is_available(self):
        return self.cooldown == 0 and self.available_uses != 0

    def process_cooldown(self):
        self.cooldown = max(self.cooldown-1, 0)

    @classmethod
    def generate_message(cls, message_type, actor_name=None, target_name=None):
        if cls.descriptions[message_type].count('%s') == 2:
            if not actor_name or not target_name:
                raise InvalidDescriptionArguments
            return cls.descriptions[message_type] % (actor_name, target_name)

        elif cls.descriptions[message_type].count('%s') == 1:
            if not actor_name:
                raise InvalidDescriptionArguments
            return cls.descriptions[message_type] % actor_name

        elif cls.descriptions[message_type].count('%s') == 0:
            return cls.descriptions[message_type]
        else:
            raise InvalidDescriptionArguments

    @property
    def total_damage(self):
        total = 0
        for damage_type in self.damage.keys():
            total += self.damage[damage_type]
        return total


class Attack(Action):
    pass


class Fists(Attack):
    name = 'Fists'
    damage = {'physical': 2}
    accuracy = 0.8
    descriptions = {
        'attempt': '%s punches %s!',
        'success': 'The punch connects with a loud thud!',
        'failure': 'The punch is easily dodged!'
    }


class Broadsword(Attack):
    name = 'Broadsword'
    damage = {'physical': 10}
    accuracy = 0.75
    descriptions = {
        'attempt': '%s swings at %s with a broadsword!',
        'success': 'The broadsword slices through %s\'s flesh!',
        'failure': 'The broadsword slices through thin air!'
    }


class PoisonedDagger(Attack):
    name = 'Poisoned Dagger'
    damage = {'physical': 5}
    applies_statuses = [(statuses.Poison, {'duration': 4, 'intensity': 4})]
    accuracy = 0.75
    descriptions = {
        'attempt': '%s stabs at %s with a poisoned dagger!',
        'success': 'The dagger plunges deep into %s\'s body, releasing poison!',
        'failure': 'The dagger is easily dodged!'
    }


class SerratedCleaver(Attack):
    name = 'Serrated Cleaver'
    damage = {'physical': 8}
    applies_statuses = [(statuses.Bleeding, {'duration': 5})]
    accuracy = 0.8
    descriptions = {
        'attempt': '%s swings at %s with a serrated cleaver!',
        'success': 'The cleaver mangles %s\'s flesh! Blood pours from the wound!',
        'failure': 'The cleaver misses %s!'
    }


class Fireball(Attack):
    name = 'Fireball'
    damage = {'fire': 15}
    cooldown_per_use = 1
    accuracy = 0.6
    descriptions = {
        'attempt': '%s throws a fireball at %s!',
        'success': 'The fireball hits with a tremendous explosion!',
        'failure': 'The fireball flies off into the distance, exploding harmlessly!',
    }


class Heal(Action):
    is_heal = True
    accuracy = 1

    @property
    def total_heal(self):
        total = 0
        for status in self.applies_statuses:
            if status[0] is statuses.Healing:
                total += status[1]['duration'] * status[1]['intensity']
        return total


class MinorHeal(Heal):
    name = 'Minor Heal'
    applies_statuses = [(statuses.Healing, {'duration': 1, 'intensity': 10})]
    cooldown_per_use = 2
    descriptions = {
        'attempt':  '%s uses Minor Heal!',
        'success': '%s\'s wounds start to close!',
        'failure': 'The healing energy fizzes and dies!',
    }


class RayOfFrost(Attack):
    name = 'Ray of Frost'
    damage = {'frost': 3}
    applies_statuses = [(statuses.Frozen, {'duration': 2})]
    accuracy = 0.6
    cooldown_per_use = 2
    descriptions = {
        'attempt': '%s casts a Ray of Frost on %s!',
        'success': 'The ray finds its target. The air around %s instantly freezes!',
        'failure': 'The ray flies off into the distance, leaving a trail of frost!',
    }


class Banhammer(Attack):
    name = 'Banhammer'
    damage = {'energy': 150}
    accuracy = 0.6
    cooldown_per_use = 1
    descriptions = {
        'attempt': '%s swings the Banhammer at %s!',
        'success': '%s\'s very existence is ripped away from this world!',
        'failure': 'The Banhammer misses %s, leaving a deep shadow in its wake!',
    }


class PitchVial(Attack):
    name = 'Vial of pitch'
    damage = {'fire': 25}
    accuracy = 0.7
    available_uses = 1
    descriptions = {
        'attempt': '%s throws a vial of pitch at %s!',
        'success': '%s is engulfed in flaming pitch!',
        'failure': 'The vial misses %s and shatters on the ground, creating a flaming pit!',
    }


def action_factory(action_class, kwargs):
    if not Action.__subclasscheck__(action_class):
        raise InvalidFactoryArgument
    return action_class(kwargs)


class InvalidFactoryArgument(Exception):
    pass


class InvalidDescriptionArguments(Exception):
    pass

