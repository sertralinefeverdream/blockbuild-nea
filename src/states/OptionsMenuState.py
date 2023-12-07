from src.states.StateBase import StateBase
from src.audio.Volume import Volume


class OptionsMenuState(StateBase):
    def __init__(self, game, GUIFactory, AudioHandlerFactory):
        super().__init__(game, GUIFactory, AudioHandlerFactory)

    def initialise_gui(self):
        self._gui = [
            {
                "exit_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.exit_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Exit"),

                "low_game_vol_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.low_game_vol_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Low"),
                "medium_game_vol_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.medium_game_vol_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Medium"),
                "high_game_vol_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.high_game_vol_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="High"),
                "game_vol_label": self._GUIFactory.create_gui("TextLabel", self._game, self._game.window, has_box=False, has_outline=False, text="Game Volume:"),

                "low_music_vol_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.low_music_vol_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Low"),
                "medium_music_vol_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.medium_music_vol_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Medium"),
                "high_music_vol_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.high_music_vol_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="High"),
                "music_vol_label": self._GUIFactory.create_gui("TextLabel", self._game, self._game.window, has_box=False, has_outline=False, text="Music Volume:")
            },
            {},
            {}
        ]



    def on_state_enter(self, *args):
        self._gui[0]["low_game_vol_button"].size = (200.0, 75.0)
        self._gui[0]["low_game_vol_button"].centre_position = (300.0, 200.0)

        self._gui[0]["medium_game_vol_button"].size = (200.0, 75.0)
        self._gui[0]["medium_game_vol_button"].centre_position = (600.0, 200.0)

        self._gui[0]["high_game_vol_button"].size = (200.0, 75.0)
        self._gui[0]["high_game_vol_button"].centre_position = (900.0, 200.0)

        self._gui[0]["game_vol_label"].font_size = 75
        self._gui[0]["game_vol_label"].centre_position = (600.0, 100.0)

        self._gui[0]["low_music_vol_button"].size = (200.0, 75.0)
        self._gui[0]["low_music_vol_button"].centre_position = (300.0, 400.0)

        self._gui[0]["medium_music_vol_button"].size = (200.0, 75.0)
        self._gui[0]["medium_music_vol_button"].centre_position = (600.0, 400.0)

        self._gui[0]["high_music_vol_button"].size = (200.0, 75.0)
        self._gui[0]["high_music_vol_button"].centre_position = (900.0, 400.0)

        self._gui[0]["exit_button"].size = (400.0, 75.0)
        self._gui[0]["exit_button"].centre_position = (600.0, 600.0)

        self._gui[0]["music_vol_label"].font_size = 75
        self._gui[0]["music_vol_label"].centre_position = (600.0, 300.0)

        self.initialise_gui_states()

    def initialise_gui_states(self):
        if self._game.get_option("game_volume").name == "LOW":
            self.low_game_vol_click(self._gui[0]["low_game_vol_button"])
        elif self._game.get_option("game_volume").name == "MEDIUM":
            self.medium_game_vol_click(self._gui[0]["medium_game_vol_button"])
        elif self._game.get_option("game_volume").name == "HIGH":
            self.high_game_vol_click(self._gui[0]["high_game_vol_button"])

        if self._game.get_option("music_volume").name == "LOW":
            self.low_music_vol_click(self._gui[0]["low_music_vol_button"])
        elif self._game.get_option("music_volume").name == "MEDIUM":
            self.medium_music_vol_click(self._gui[0]["medium_music_vol_button"])
        elif self._game.get_option("music_volume").name == "HIGH":
            self.high_music_vol_click(self._gui[0]["high_music_vol_button"])

    def on_state_leave(self, *args):
        pass

    def update(self):
        self._game.window.fill((255, 255, 255))
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()

    def exit_click(self, button):
        self._game.pop_state()

    def low_game_vol_click(self, button):
        self._gui[0]["low_game_vol_button"].button_colour = (255, 255, 0)
        self._gui[0]["low_game_vol_button"].hover_colour = (127, 127, 0)

        self._gui[0]["medium_game_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["medium_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["high_game_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["high_game_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("game_volume", Volume.LOW)

    def medium_game_vol_click(self, button):
        self._gui[0]["low_game_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["low_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["medium_game_vol_button"].button_colour = (255, 255, 0)
        self._gui[0]["medium_game_vol_button"].hover_colour = (127, 127, 0)

        self._gui[0]["high_game_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["high_game_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("game_volume", Volume.MEDIUM)

    def high_game_vol_click(self, button):
        self._gui[0]["low_game_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["low_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["medium_game_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["medium_game_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["high_game_vol_button"].button_colour = (255, 255, 0)
        self._gui[0]["high_game_vol_button"].hover_colour = (127, 127, 0)

        self._game.set_option("game_volume", Volume.HIGH)

    def low_music_vol_click(self, button):
        self._gui[0]["low_music_vol_button"].button_colour = (255, 255, 0)
        self._gui[0]["low_music_vol_button"].hover_colour = (127, 127, 0)

        self._gui[0]["medium_music_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["medium_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["high_music_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["high_music_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("music_volume", Volume.LOW)

    def medium_music_vol_click(self, button):
        self._gui[0]["low_music_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["low_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["medium_music_vol_button"].button_colour = (255, 255, 0)
        self._gui[0]["medium_music_vol_button"].hover_colour = (127, 127, 0)

        self._gui[0]["high_music_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["high_music_vol_button"].hover_colour = (127, 0, 0)

        self._game.set_option("music_volume", Volume.MEDIUM)

    def high_music_vol_click(self, button):
        self._gui[0]["low_music_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["low_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["medium_music_vol_button"].button_colour = (255, 0, 0)
        self._gui[0]["medium_music_vol_button"].hover_colour = (127, 0, 0)

        self._gui[0]["high_music_vol_button"].button_colour = (255, 255, 0)
        self._gui[0]["high_music_vol_button"].hover_colour = (127, 127, 0)

        self._game.set_option("music_volume", Volume.HIGH)

