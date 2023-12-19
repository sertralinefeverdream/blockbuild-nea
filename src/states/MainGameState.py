from src.states.StateBase import StateBase
from src.world.RegionGenerator import RegionGenerator
from src.world.World import World


class MainGameState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._world = World(game, RegionGenerator())


    def initialise_gui(self):
        self._gui = [
            {},
            {},
            {}
        ]

    def on_state_enter(self):
        pass

    def on_state_leave(self):
        pass

    def update(self):
        self._game.window.fill((255, 255, 255))
        self._world.draw()
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()
