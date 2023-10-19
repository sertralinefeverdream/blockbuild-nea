from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton
import random


class MainMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {
            "options_button":TextButton(self._game.window, 300.0, 400.0, 150.0, 75.0, text="Options", click_func=self.options_button_click, outline_colour=(0, 0, 0), button_colour=(255, 0, 0)),
            "exit_button":TextButton(self._game.window, 600.0, 400.0, 150.0, 75.0, text="Exit!", click_func=self.exit_button_click, outline_colour=(0, 0, 0), button_colour=(255, 0, 0))
        }

    def on_state_enter(self):
        print("Entered state!")

    def on_state_leave(self):
        print("Left state")

    def loop(self):
        self._game.window.fill((255, 255, 255))
        for component in self._gui.values():  # Iterates through all guis in dict and updates and draws them
            component.update()
            if component.is_visible:
                component.draw()

    def options_button_click(self, button):
        self._game.push_state("options_menu")

    def options_button_hold(self, button):
        button.font_size += 1

    def exit_button_click(self, button):
        self._game.pop_state()