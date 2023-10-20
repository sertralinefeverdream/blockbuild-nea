from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton
from src.gui.TextLabel import TextLabel
import random


class MainMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {
            "options_button":TextButton(self._game.window, self.options_button_click, size=(400.0, 75.0), text="Options", outline_colour=(0, 0, 0), button_colour=(255, 0, 0), hover_colour=(200, 0, 0)),
            "exit_button":TextButton(self._game.window, self.exit_button_click, size=(400.0, 75.0), text="Exit!", outline_colour=(0, 0, 0), button_colour=(255, 0, 0), hover_colour=(200, 0, 0)),
            "play_button":TextButton(self._game.window, self.play_button_click, size=(400.0, 75.0), text="Play!", outline_colour=(0, 0, 0), button_colour=(255, 0 ,0), hover_colour=(200, 0 ,0)),
            "label":TextLabel(self._game.window, has_box=False, font_size=100)
        }

    def on_state_enter(self):
        print("Entered state!")
        self._gui["play_button"].centre_position = (600.0, 300.0)
        self._gui["options_button"].centre_position = (600.0, 400.0)
        self._gui["exit_button"].centre_position = (600.0, 500.0)
        self._gui["label"].size = (400.0, 125.0)
        self._gui["label"].centre_position = (600.0, 100.0)

    def on_state_leave(self):
        pass

    def loop(self):
        self._game.window.fill((255, 255, 255))
        for component in self._gui.values():  # Iterates through all guis in dict and updates and draws them
            component.update()
            component.draw()

    def options_button_click(self, button):
        self._game.push_state("options_menu")

    def play_button_click(self, button):
        pass

    def exit_button_click(self, button):
        self._game.pop_state()