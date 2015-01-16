class Status(object):
    status_applied_message = ''
    effect_applied_message = ''
    status_removed_message = ''

    def __init__(self, name=None, duration=1):
        self.name = name if name else 'Generic Status'
        self.duration = duration

    def apply_to_actor(self, actor):
        self.actor_affected = actor
        if self not in self.actor_affected.statuses:
            if self.status_applied_message:
                print self.status_applied_message % self.actor_affected.name
            self.actor_affected.statuses.append(self)

    def apply_effect_and_check_duration(self):
        if self.effect_applied_message:
            print self.effect_applied_message % self.actor_affected.name
        self._apply_effect()
        if self.duration <= 0:
            self._remove_from_actor()

    def _remove_from_actor(self):
        if self in self.actor_affected.statuses:
            if self.status_removed_message:
                print self.status_removed_message % self.actor_affected.name
            self.actor_affected.statuses.remove(self)

    def _apply_effect(self):
        pass


class Poison(Status):
    status_applied_message = '%s has been poisoned!'
    effect_applied_message = '%s suffers poison damage!'
    status_removed_message = '%s has recovered from poison!'

    def __init__(self, duration, intensity):
        Status.__init__(self, name='Poisoned', duration=duration)
        self.intensity = intensity

    def _apply_effect(self):
        self.actor_affected._modify_hp(-self.intensity)
        self.duration -= 1


class Bleeding(Status):
    status_applied_message = '%s has started bleeding!'
    effect_applied_message = '%s suffers bleed damage!'
    status_removed_message = '%s has stopped bleeding!'

    def __init__(self, duration):
        Status.__init__(self, name='Bleeding', duration=duration)

    def _apply_effect(self):
        self.actor_affected._modify_hp(-self.duration)
        self.duration -= 1


class Frozen(Status):
    status_applied_message = '%s has been encased in ice!'
    status_removed_message = '%s has thawed!'

    def __init__(self, duration):
        Status.__init__(self, name='Frozen', duration=duration)

    def apply_to_actor(self, actor):
        self.actor_affected = actor
        if self not in self.actor_affected.statuses:
            print self.status_applied_message % self.actor_affected.name
            self.actor_affected.statuses.append(self)
            self.actor_affected.can_act = False

    def _apply_effect(self):
        self.duration -= 1

    def _remove_from_actor(self):
        if self in self.actor_affected.statuses:
            print self.status_removed_message % self.actor_affected.name
            self.actor_affected.statuses.remove(self)
            self.actor_affected.can_act = True



class Death(Status):
    status_applied_message = '%s has died!'

    def __init__(self):
        Status.__init__(self, name='Dead', duration=1)

    def apply_to_actor(self, actor):
        self.actor_affected = actor
        if self not in self.actor_affected.statuses:
            print self.status_applied_message % self.actor_affected.name
            self.actor_affected.statuses = [self]

