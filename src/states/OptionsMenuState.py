from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton


class OptionsMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {"exit_button":TextButton(self._game.window, self.foo, (300.0, 400.0), (400.0, 75.0), text="Exit!", outline_colour=(0, 0, 0), button_colour=(255, 0, 0), hover_colour=(200, 200, 200))}

    def on_state_enter(self):
        self._gui["exit_button"].centre_position = (600.0, 600.0)

    def on_state_leave(self):
        pass

    def loop(self):
        self._game.window.fill((120, 120, 120))
        for component in self._gui.values():  # Iterates through all guis in dict and updates and draws them
            component.update()
            component.draw()

    def foo(self, button):
        self._game.pop_state()