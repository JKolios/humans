from random import choice, randint

import actors
import battle

""" TODO: add new statuses(STUUUNNN), Heals and heal target logic?, Random events per turn."""

DEFAULT_ACTOR_LIST = [
    actors.Thief('Alice'),
    actors.Warrior('Bob'),
    actors.Mage('Charles'),
    actors.Priest('Derek'),
    actors.Brigand('Ed'),
    # actors.Devastator('Fred'),
    actors.Grenadier('Garry')
]

NAME_LIST = ['Alice', 'Bob', 'Charles', 'Derek', 'Ed', 'Fred', 'Garry', 'Harold', 'Ian', 'James', 'Karen', 'Larry',
             'Mary', 'Nadia', 'Omar', 'Percy', 'Quincy', 'Red', 'Sally', 'Thalia', 'Una', 'Victor', 'Warren', 'Xavier',
             'Yahn', 'Zidane']


def random_actor_list():
    actor_list = []
    actor_count = randint(2, 6)
    for i in range(actor_count):
        random_actor = choice(list(actors.Actor.registry))(choice(NAME_LIST))
        print random_actor
        actor_list.append(random_actor)
    return actor_list


if __name__ == '__main__':
    handler = battle.Battlehandler(random_actor_list())
    handler.run_turns()


