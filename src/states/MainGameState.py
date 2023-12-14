from src.states.StateBase import StateBase

class MainGameState(StateBase):
    def __init__(self, game, gui_factory, audio_handler_factory, block_factory):
        super().__init__(game, gui_factory, audio_handler_factory)
        self._block_factory = block_factory
        self._world = None
        self._block_1 = None
        self._block_2 = None

    def initialise_gui(self):
        self._gui = [
            {},
            {},
            {}
        ]

    def on_state_enter(self):
        self._block_1 = self._block_factory.create_block(self._game, "grass")
        self._block_2 = self._block_factory.create_block(self._game, "grass")

    def on_state_leave(self):
        pass

    def update(self):
        self._game.window.fill((255, 255, 255))
        self._block_1.draw((0, 0))
        self._block_2.draw((40, 0))
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()
