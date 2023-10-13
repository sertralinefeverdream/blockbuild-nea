from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton


class OptionsMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {"exit_button":TextButton(self._game.window, 300.0, 400.0, 150.0, 75.0, text="Exit!", click_func=self.foo, held_func=None, outline_colour=(0, 0, 0), button_colour=(0, 255, 0))}

    def on_state_enter(self):
        pass

    def on_state_leave(self):
        pass

    def loop(self):
        self._game.window.fill((120, 120, 120))
        for component in self._gui.values():  # Iterates through all guis in dict and updates and draws them
            component.update()
            if component.is_visible:
                component.draw()

    def foo(self, button):
        self._game.pop_state()