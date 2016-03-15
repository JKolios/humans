from .exceptions import InvalidStatusDuration
from metaclasses import RegisterLeafClasses
import constants


class Status(object, metaclass=RegisterLeafClasses):
    status_applied_message = ''
    effect_applied_message = ''
    status_removed_message = ''

    def __init__(self, duration=1):
        self.duration = duration
        self.actor_affected = None

    def apply_to_actor(self, actor):
        self.actor_affected = actor
        # Do not apply the same effect object twice
        if self not in self.actor_affected.effects:
            if self.status_applied_message:
                print(self.status_applied_message % self.actor_affected.name)
            self.actor_affected.effects.append(self)

    def apply_effect_and_check_duration(self):
        if self.effect_applied_message:
            print(self.effect_applied_message % self.actor_affected.name)
        self._apply_effect()
        if self.duration == 0:
            self._remove_from_actor()
        elif self.duration < 0:
            raise InvalidStatusDuration

    def _remove_from_actor(self):
        if self in self.actor_affected.effects:
            if self.status_removed_message:
                print(self.status_removed_message % self.actor_affected.name)
            self.actor_affected.effects.remove(self)

    def _apply_effect(self):
        pass


class Poison(Status):
    status_applied_message = '%s has been poisoned!'
    effect_applied_message = '%s suffers poison damage!'
    status_removed_message = '%s has recovered from poison!'

    def __init__(self, kwargs):
        self.duration = kwargs['duration']
        self.intensity = kwargs['intensity']
        self.name = 'Poisoned'
        Status.__init__(self, duration=self.duration)

    def _apply_effect(self):
        self.actor_affected.modify_hp(-self.intensity)
        self.duration -= 1


class Bleeding(Status):
    status_applied_message = '%s has started bleeding!'
    effect_applied_message = '%s suffers bleed damage!'
    status_removed_message = '%s has stopped bleeding!'

    def __init__(self, kwargs):
        self.duration = kwargs['duration']
        self.name = 'Bleeding'
        Status.__init__(self, duration=self.duration)

    def _apply_effect(self):
        self.actor_affected.modify_hp(-self.duration)
        self.duration -= 1


class Frozen(Status):
    status_applied_message = '%s has been encased in ice!'
    status_removed_message = '%s has thawed!'

    def __init__(self, kwargs):
        self.duration = kwargs['duration']
        self.name = 'Frozen'
        Status.__init__(self, duration=self.duration)

    def apply_to_actor(self, actor):
        self.actor_affected = actor
        if self not in self.actor_affected.effects:
            print(self.status_applied_message % self.actor_affected.name)
            self.actor_affected.effects.append(self)
            self.actor_affected.can_act = False

    def _apply_effect(self):
        self.duration -= 1

    def _remove_from_actor(self):
        if self in self.actor_affected.effects:
            print(self.status_removed_message % self.actor_affected.name)
            self.actor_affected.effects.remove(self)
            self.actor_affected.can_act = True


class Healing(Status):
    effect_applied_message = '%s is being healed!'

    def __init__(self, kwargs):
        self.duration = kwargs['duration']
        self.intensity = kwargs['intensity']
        self.name = 'Healing'
        Status.__init__(self, duration=self.duration)

    def _apply_effect(self):
        self.actor_affected.modify_hp(self.intensity)
        self.duration -= 1


class Death(Status):
    status_applied_message = '%s has died!'

    def __init__(self):
        Status.__init__(self, duration=constants.INFINITE)

    def apply_to_actor(self, actor):
        self.actor_affected = actor
        if self not in self.actor_affected.effects:
            print(self.status_applied_message % self.actor_affected.name)
            self.actor_affected.effects = [self]


def status_factory(status_class, kwargs):
    return status_class(kwargs)
