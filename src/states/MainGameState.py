from StateBase import StateBase


class MainGameState(StateBase):
    def __init__(self, game, gui_factory, audio_handler_factory):
        super().__init__(game, gui_factory, audio_handler_factory)

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
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()
