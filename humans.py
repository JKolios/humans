import creatures
from battle_handler import Battlehandler

""" TODO: add new statuses(STUUUNNN), Heals and heal target logic?, Random events per turn, review damage types,
ACCURACY."""

DEFAULT_ACTOR_LIST = [creatures.Thief('Alice'),
                      creatures.Warrior('Bob'),
                      creatures.Mage('Charles'),
                      creatures.Priest('Derek'),
                      creatures.Brigand('Ed'),
                      # creatures.Devastator('Fred')
]


if __name__ == '__main__':
    handler = Battlehandler(DEFAULT_ACTOR_LIST)
    handler.run_turns()



