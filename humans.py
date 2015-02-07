import actors
from battle.battle_handler import Battlehandler

""" TODO: add new statuses(STUUUNNN), Heals and heal target logic?, Random events per turn."""

DEFAULT_ACTOR_LIST = [actors.Thief('Alice'),
                      actors.Warrior('Bob'),
                      actors.Mage('Charles'),
                      actors.Priest('Derek'),
                      actors.Brigand('Ed'),
                      # actors.Devastator('Fred'),
                      actors.Grenadier('Garry')
]

if __name__ == '__main__':
    handler = Battlehandler(DEFAULT_ACTOR_LIST)
    handler.run_turns()



