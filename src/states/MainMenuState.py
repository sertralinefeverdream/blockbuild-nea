from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton
from src.gui.TextLabel import TextLabel
import random


class MainMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {
            "options_button":TextButton(self._game.window, self.options_button_click, self._game.audiohandler, text="Options"),
            "exit_button":TextButton(self._game.window, self.exit_button_click, self._game.audiohandler, text="Exit"),
            "play_button":TextButton(self._game.window, self.play_button_click, self._game.audiohandler, text="Play"),
            "logo":TextLabel(self._game.window, has_box=False, font_size=100)
        }

    def on_state_enter(self):
      #  print("Entered state!")
        self._game.audiohandler.set_shuffle_list(["main_menu"])
        if self._game.previous_state is not self._game.states["main_menu"]:
            self._game.audiohandler.shuffle_play()

        self._gui["play_button"].size = (400.0, 75.0)
        self._gui["options_button"].size = (400.0, 75.0)
        self._gui["exit_button"].size = (400.0, 75.0)

        self._gui["play_button"].font_size = 45
        self._gui["options_button"].font_size = 45
        self._gui["exit_button"].font_size = 45

        self._gui["play_button"].centre_position = (600.0, 300.0)
        self._gui["options_button"].centre_position = (600.0, 400.0)
        self._gui["exit_button"].centre_position = (600.0, 500.0)

        self._gui["logo"].centre_position = (600.0, 100.0)

        self._gui["play_button"].is_enabled = False

    def on_state_leave(self):
        pass
        #print("leaving!")

    def loop(self):
        self._game.window.fill((255, 255, 255))
       # print(self._game.previous_state)
        for component in self._gui.values():  # Iterates through all guis in dict and updates and draws them
            component.update()
            component.draw()

    def options_button_click(self, button):
        self._game.push_state("options_menu")

    def play_button_click(self, button):
        pass

    def exit_button_click(self, button):
        self._game.pop_state()
