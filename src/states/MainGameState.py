from src.states.StateBase import StateBase


class MainGameState(StateBase):
    def __init__(self, game, world):
        super().__init__(game)
        self._world = world
        self._step = 0

    def initialise_gui(self):
        self._gui = [
            {},
            {},
            {}
        ]

    def on_state_enter(self):
        for x in range(20):
            for y in range(20):
                if y > 15:
                    self._world.set_block_at_position((x*40, y*40), "grass")

    def on_state_leave(self):
        pass

    def update(self):
        self._game.window.fill((0, 0, 0))
        self._world.update()
        self._world.draw()

        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()
