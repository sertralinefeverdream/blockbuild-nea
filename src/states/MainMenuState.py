from states.StateBase import StateBase

#uploaded

class MainMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)

    def initialise_gui(self):
        self._gui = [
            {
                "options_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                    self.options_button_click, text="Options"),
                "exit_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                 self.exit_button_click,
                                                                 text="Exit"),
                "play_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                 self.play_button_click,
                                                                 text="Play"),
                "logo": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window, has_box=False,
                                                          has_outline=False, font_size=100, text="BlockBuild!",
                                                          font_name="bahnschrift")
            },
            {},
            {}
        ]

    def on_state_enter(self, params=None):
        self._game.music_handler.set_shuffle_list(["At Tesko This Week"])
        # print(self._game.previous_state)
        if self._game.previous_state is not self._game.states["load_game_menu"]:
            self._game.music_handler.shuffle_play()

        self._gui[0]["play_button"].size = (400.0, 75.0)
        self._gui[0]["options_button"].size = (400.0, 75.0)
        self._gui[0]["exit_button"].size = (400.0, 75.0)

        self._gui[0]["play_button"].font_size = 45
        self._gui[0]["options_button"].font_size = 45
        self._gui[0]["exit_button"].font_size = 45

        self._gui[0]["play_button"].centre_position = (600.0, 300.0)
        self._gui[0]["options_button"].centre_position = (600.0, 400.0)
        self._gui[0]["exit_button"].centre_position = (600.0, 500.0)

        self._gui[0]["logo"].centre_position = (600.0, 100.0)

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def on_state_leave(self, params=None):
        print("LEAVING MAIN MENU STATE")

    def update(self):
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()

    def draw(self, no_gui=False):
        self._game.window.fill((255, 255, 255))
        if not no_gui:
            for layer in self._gui[::-1]:
                for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                    component.draw()

    def options_button_click(self, button):
        self._game.push_state("options_menu")

    def play_button_click(self, button):
        self._game.push_state("load_game_menu")

    def exit_button_click(self, button):
        self._game.pop_state()
