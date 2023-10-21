from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton
from src.gui.TextLabel import TextLabel
import random


class MainMenuState(StateBase):
    def __init__(self, game, music_assets={}, sfx_assets={}):
        super().__init__(game, music_assets, sfx_assets)
        self._gui = {
            "options_button":TextButton(self._game.window, self.options_button_click, "btn_click_1", "btn_click_1", "btn_click_1", self._game.audiohandler, size=(400.0, 75.0), text="Options", outline_colour=(0, 0, 0), button_colour=(255, 0, 0), hover_colour=(200, 0, 0)),
            "exit_button":TextButton(self._game.window, self.exit_button_click, "btn_click_1", "btn_click_1", "btn_click_1", self._game.audiohandler, size=(400.0, 75.0), text="Exit!", outline_colour=(0, 0, 0), button_colour=(255, 0, 0), hover_colour=(200, 0, 0)),
            "play_button":TextButton(self._game.window, self.play_button_click, "btn_click_1", "btn_click_1", "btn_click_1", self._game.audiohandler, size=(400.0, 75.0), text="Play!", outline_colour=(0, 0, 0), button_colour=(255, 0 ,0), hover_colour=(200, 0 ,0)),
            "logo":TextLabel(self._game.window, has_box=False, font_size=100)
        }
        self.initialise_sfx_and_music()

    def initialise_sfx_and_music(self):
        self._game.audiohandler.add_sfx_from_dict(self._sfx_assets)
        self._game.audiohandler.add_music_from_dict(self._music_assets)

    def on_state_enter(self):
      #  print("Entered state!")
        self._game.audiohandler.set_music_list(["main_menu"])
        if self._game.previous_state is not self._game.states["main_menu"]:
            self._game.audiohandler.play_from_music_list("main_menu")

        self._gui["play_button"].centre_position = (600.0, 300.0)
        self._gui["options_button"].centre_position = (600.0, 400.0)
        self._gui["exit_button"].centre_position = (600.0, 500.0)
        self._gui["logo"].centre_position = (600.0, 100.0)

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
