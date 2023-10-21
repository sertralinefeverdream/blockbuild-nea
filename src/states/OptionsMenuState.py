from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton
from src.gui.TextLabel import TextLabel


class OptionsMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {
            "exit_button":TextButton(self._game.window, self.exit_click, self._game.audiohandler, text="Exit"),

            "low_game_vol_button":TextButton(self._game.window, self.low_game_vol_click, self._game.audiohandler, text="Low"),
            "medium_game_vol_button":TextButton(self._game.window, self.medium_game_vol_click, self._game.audiohandler, text="Medium"),
            "high_game_vol_button":TextButton(self._game.window, self.high_game_vol_click, self._game.audiohandler, text="High"),
            "game_vol_label": TextLabel(self._game.window, has_box=False, has_outline=False, text="Game Volume:"),

            "low_music_vol_button":TextButton(self._game.window, self.low_music_vol_click, self._game.audiohandler, text="Low"),
            "medium_music_vol_button":TextButton(self._game.window, self.medium_music_vol_click, self._game.audiohandler, text="Medium"),
            "high_music_vol_button":TextButton(self._game.window, self.high_music_vol_click, self._game.audiohandler, text="High"),
            "music_vol_label": TextLabel(self._game.window, has_box=False, has_outline=False, text="Music Volume:")

        }

    def on_state_enter(self):
        self._gui["low_game_vol_button"].size = (200.0, 75.0)
        self._gui["low_game_vol_button"].centre_position = (300.0, 200.0)

        self._gui["medium_game_vol_button"].size = (200.0, 75.0)
        self._gui["medium_game_vol_button"].centre_position = (600.0, 200.0)

        self._gui["high_game_vol_button"].size = (200.0, 75.0)
        self._gui["high_game_vol_button"].centre_position = (900.0, 200.0)

        self._gui["game_vol_label"].font_size = 75
        self._gui["game_vol_label"].centre_position = (600.0, 100.0)

        self._gui["low_music_vol_button"].size = (200.0, 75.0)
        self._gui["low_music_vol_button"].centre_position = (300.0, 400.0)

        self._gui["medium_music_vol_button"].size = (200.0, 75.0)
        self._gui["medium_music_vol_button"].centre_position = (600.0, 400.0)

        self._gui["high_music_vol_button"].size = (200.0, 75.0)
        self._gui["high_music_vol_button"].centre_position = (900.0, 400.0)

        self._gui["exit_button"].size = (400.0, 75.0)
        self._gui["exit_button"].centre_position = (600.0, 600.0)

        self._gui["music_vol_label"].font_size = 75
        self._gui["music_vol_label"].centre_position = (600.0, 300.0)

        self.initialise_gui_states()

    def initialise_gui_states(self):
        if self._game.get_option("game_volume") == "low":
            self.low_game_vol_click(self._gui["low_game_vol_button"])
        elif self._game.get_option("game_volume") == "medium":
            self.medium_game_vol_click(self._gui["medium_game_vol_button"])
        elif self._game.get_option("game_volume") == "high":
            self.high_game_vol_click(self._gui["high_game_vol_button"])

        if self._game.get_option("music_volume") == "low":
            self.low_music_vol_click(self._gui["low_music_vol_button"])
        elif self._game.get_option("music_volume") == "medium":
            self.medium_music_vol_click(self._gui["medium_music_vol_button"])
        elif self._game.get_option("music_volume") == "high":
            self.high_music_vol_click(self._gui["high_music_vol_button"])

    def on_state_leave(self):
        pass

    def loop(self):
        #print(self._game.previous_state)
        self._game.window.fill((255, 255, 255))
        for component in self._gui.values():  # Iterates through all guis in dict and updates and draws them
            component.update()
            component.draw()

    def exit_click(self, button):
        self._game.pop_state()

    def low_game_vol_click(self, button):
        self._gui["low_game_vol_button"].button_colour = (255, 255, 0)
        self._gui["low_game_vol_button"].hover_colour = (127, 127, 0)

        self._gui["medium_game_vol_button"].button_colour = (255, 0, 0)
        self._gui["medium_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui["high_game_vol_button"].button_colour = (255, 0, 0)
        self._gui["high_game_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("game_volume", "low")
        self._game.audiohandler.update_volumes()

    def medium_game_vol_click(self, button):
        self._gui["low_game_vol_button"].button_colour = (255, 0, 0)
        self._gui["low_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui["medium_game_vol_button"].button_colour = (255, 255, 0)
        self._gui["medium_game_vol_button"].hover_colour = (127, 127, 0)

        self._gui["high_game_vol_button"].button_colour = (255, 0, 0)
        self._gui["high_game_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("game_volume", "medium")
        self._game.audiohandler.update_volumes()

    def high_game_vol_click(self, button):
        self._gui["low_game_vol_button"].button_colour = (255, 0, 0)
        self._gui["low_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui["medium_game_vol_button"].button_colour = (255, 0, 0)
        self._gui["medium_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui["high_game_vol_button"].button_colour = (255, 255, 0)
        self._gui["high_game_vol_button"].hover_colour = (127, 127, 0)

        self._game.set_option("game_volume", "high")
        self._game.audiohandler.update_volumes()

    def low_music_vol_click(self, button):
        self._gui["low_music_vol_button"].button_colour = (255, 255, 0)
        self._gui["low_music_vol_button"].hover_colour = (127, 127, 0)

        self._gui["medium_music_vol_button"].button_colour = (255, 0, 0)
        self._gui["medium_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui["high_music_vol_button"].button_colour = (255, 0, 0)
        self._gui["high_music_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("music_volume", "low")
        self._game.audiohandler.update_volumes()

    def medium_music_vol_click(self, button):
        self._gui["low_music_vol_button"].button_colour = (255, 0, 0)
        self._gui["low_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui["medium_music_vol_button"].button_colour = (255, 255, 0)
        self._gui["medium_music_vol_button"].hover_colour = (127, 127, 0)

        self._gui["high_music_vol_button"].button_colour = (255, 0, 0)
        self._gui["high_music_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("music_volume", "medium")
        self._game.audiohandler.update_volumes()

    def high_music_vol_click(self, button):
        self._gui["low_music_vol_button"].button_colour = (255, 0, 0)
        self._gui["low_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui["medium_music_vol_button"].button_colour = (255, 0, 0)
        self._gui["medium_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui["high_music_vol_button"].button_colour = (255, 255, 0)
        self._gui["high_music_vol_button"].hover_colour = (127, 127, 0)

        self._game.set_option("music_volume", "high")
        self._game.audiohandler.update_volumes()

