import actors


class InvalidActor(Exception):
    pass


class Battlehandler(object):
    def __init__(self, actor_list):

        self._validate_actor_list(actor_list)
        self.actors = actor_list
        self.active_actors = self.actors[:]

        self.turn_number = 0

    def _turn_loop(self):
        print '\nTurn %s begins!' % self.turn_number
        for actor in self.active_actors:
            if actor.can_act:
                available_targets = [target for target in self.active_actors if target is not actor]
                try:
                    actor.attack(available_targets=available_targets)
                except actors.Death as e:
                    self.active_actors.remove(e.dead_creature)
                    if e.dead_creature is actor:
                        continue
            try:
                actor.process_statuses()
            except actors.Death as e:
                self.active_actors.remove(e.dead_creature)
                if e.dead_creature is actor:
                    continue

            actor.process_cooldowns()

        self.turn_number += 1

    def run_turns(self):
        self.turn_number = 1
        while len(self.active_actors) > 1:
            self._turn_loop()
        if len(self.active_actors) == 1:
            print '%s has conquered!' % self.active_actors[0].name
            print '\nLast fighter standing\n%s' % self.active_actors[0]
        elif len(self.active_actors) == 0:
            print 'There were no survivors!'

    @staticmethod
    def _validate_actor_list(actor_list):
            for actor in actor_list:
                if not issubclass(actor.__class__, actors.Actor):
                    raise InvalidActor

