import creatures

DEFAULT_ACTOR_LIST = [creatures.Thief('Alice'),
                      creatures.Warrior('Bob'),
                      creatures.Mage('Charles')]


class InvalidActor(Exception):
    pass


class Battlehandler(object):
    def __init__(self, actors=DEFAULT_ACTOR_LIST):
        try:
            self._validate_actor_list(actors)
        except InvalidActor:
            print 'Invalid initial actor list, using default'
            self.actors = DEFAULT_ACTOR_LIST
        self.actors = actors
        self.active_actors = self.actors[:]

        self.turn_number = 0

    def _turn_loop(self):
        print '\nTurn %s begins!' % self.turn_number
        for actor in self.active_actors:
            if actor.can_act:
                available_targets = [target for target in self.active_actors if target is not actor]
                try:
                    actor.attack(available_targets=available_targets)
                except creatures.Death as e:
                    self.active_actors.remove(e.dead_creature)
                    if e.dead_creature is actor:
                        continue
            try:
                actor.process_statuses()
            except creatures.Death as e:
                self.active_actors.remove(e.dead_creature)
                if e.dead_creature is actor:
                    continue

        self.turn_number += 1

    def run_turns(self):
        self.turn_number = 1
        while len(self.active_actors) > 1:
            self._turn_loop()
        print '%s has conquered!' % self.active_actors[0].name



    @staticmethod
    def _validate_actor_list(actor_list):
            for actor in actor_list:
                if not issubclass(actor.__class__, creatures.Creature):
                    raise InvalidActor

