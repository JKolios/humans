from random import choice, randint

import character_classes
import battle

""" TODO: add new effects(STUUUNNN), Heals and heal target logic?, Random events per turn."""

DEFAULT_ACTOR_LIST = [
    character_classes.Thief('Alice'),
    character_classes.Warrior('Bob'),
    character_classes.Mage('Charles'),
    character_classes.Priest('Derek'),
    character_classes.Brigand('Ed'),
    # character_classes.Devastator('Fred'),
    character_classes.Grenadier('Garry')
]

NAME_LIST = ['Alice', 'Bob', 'Charles', 'Derek', 'Ed', 'Fred', 'Garry', 'Harold', 'Ian', 'James', 'Karen', 'Larry',
             'Mary', 'Nadia', 'Omar', 'Percy', 'Quincy', 'Red', 'Sally', 'Thalia', 'Una', 'Victor', 'Warren', 'Xavier',
             'Yahn', 'Zidane']


def random_actor_list():
    actor_list = []
    actor_count = randint(2, 6)
    for i in range(actor_count):
        random_actor = choice(list(character_classes.CharacterClass.registry))(choice(NAME_LIST))
        print(random_actor)
        actor_list.append(random_actor)
    return actor_list


if __name__ == '__main__':
    handler = battle.Battlehandler(DEFAULT_ACTOR_LIST)
    handler.run_turns()


