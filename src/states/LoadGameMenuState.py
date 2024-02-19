from states.StateBase import StateBase

#uploaded

class LoadGameMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)

    def initialise_gui(self):
        self._gui = [
            {
                "top_save_label": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window,
                                                                    text="Save 1:"),
                "top_load_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                     self.load_button_func, text="Load"),
                "top_new_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                    self.new_button_func, text="New"),

                "middle_save_label": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window,
                                                                       text="Save 2:"),
                "middle_load_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                        self.load_button_func, text="Load"),
                "middle_new_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                       self.new_button_func, text="New"),

                "bottom_save_label": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window,
                                                                       text="Save 3:"),
                "bottom_load_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                        self.load_button_func, text="Load"),
                "bottom_new_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                       self.new_button_func, text="New"),

                "exit_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                 self.exit_click, text="Exit")
            },
            {},
            {
                "top_box": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window),
                "middle_box": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window),
                "bottom_box": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window)

            }
        ]

    def on_state_enter(self, params=None):
        self._game.music_handler.set_shuffle_list(["At Tesko This Week"])
        if self._game.previous_state is not self._game.states["main_menu"]:
            self._game.shuffle_play()

        self._gui[0]["exit_button"].size = (400.0, 75.0)
        self._gui[0]["exit_button"].centre_position = (600.0, 600.0)

        self._gui[0]["top_save_label"].font_size = 60
        self._gui[0]["top_save_label"].font_name = "bahnschrift"
        self._gui[0]["top_save_label"].conform_overhang_to_size((250.0, 75.0))
        self._gui[0]["top_save_label"].centre_position = (412.5, 100.0)

        self._gui[2]["top_box"].size = (800.0, 150.0)
        self._gui[2]["top_box"].centre_position = (600.0, 100.0)
        self._gui[2]["top_box"].box_colour = (200, 200, 200)

        self._gui[0]["top_new_button"].size = (150.0, 100.0)
        self._gui[0]["top_new_button"].font_size = 50
        self._gui[0]["top_new_button"].centre_position = (700.0, 100.0)

        self._gui[0]["top_load_button"].size = (150.0, 100.0)
        self._gui[0]["top_load_button"].font_size = 50
        self._gui[0]["top_load_button"].centre_position = (875.0, 100.0)

        self._gui[0]["middle_save_label"].font_size = 60
        self._gui[0]["middle_save_label"].font_name = "bahnschrift"
        self._gui[0]["middle_save_label"].conform_overhang_to_size((250.0, 75.0))
        self._gui[0]["middle_save_label"].centre_position = (412.5, 275.0)

        self._gui[2]["middle_box"].size = (800.0, 150.0)
        self._gui[2]["middle_box"].size = (800.0, 150.0)
        self._gui[2]["middle_box"].centre_position = (600.0, 275.0)
        self._gui[2]["middle_box"].box_colour = (200, 200, 200)

        self._gui[0]["middle_new_button"].size = (150.0, 100.0)
        self._gui[0]["middle_new_button"].font_size = 50
        self._gui[0]["middle_new_button"].centre_position = (700.0, 275.0)

        self._gui[0]["middle_load_button"].size = (150.0, 100.0)
        self._gui[0]["middle_load_button"].font_size = 50
        self._gui[0]["middle_load_button"].centre_position = (875.0, 275.0)

        self._gui[0]["bottom_save_label"].font_size = 60
        self._gui[0]["bottom_save_label"].font_name = "bahnschrift"
        self._gui[0]["bottom_save_label"].conform_overhang_to_size((250.0, 75.0))
        self._gui[0]["bottom_save_label"].centre_position = (412.5, 450.0)

        self._gui[2]["bottom_box"].size = (800.0, 150.0)
        self._gui[2]["bottom_box"].centre_position = (600.0, 450.0)
        self._gui[2]["bottom_box"].box_colour = (200, 200, 200)

        self._gui[0]["bottom_new_button"].size = (150.0, 100.0)
        self._gui[0]["bottom_new_button"].font_size = 50
        self._gui[0]["bottom_new_button"].centre_position = (700.0, 450.0)

        self._gui[0]["bottom_load_button"].size = (150.0, 100.0)
        self._gui[0]["bottom_load_button"].font_size = 50
        self._gui[0]["bottom_load_button"].centre_position = (875.0, 450.0)

        for layer in self._gui[::-1]:  # Iterates through all guis in dict and updates and draws them
            for component in layer.values():
                component.update()

    def on_state_leave(self, params=None):
        print(f"LEAVING LOAD GAME STATE")

    def update(self):
        for layer in self._gui[::-1]:  # Iterates through all guis in dict and updates and draws them
            for component in layer.values():
                component.update()

    def draw(self, no_gui=False):
        self._game.window.fill((255, 255, 255))
        if not no_gui:
            for layer in self._gui[::-1]:
                for component in layer.values():
                    component.draw()

    def new_button_func(self, button):
        if button is self._gui[0]["top_new_button"]:
            self._game.pop_state()
            self._game.push_state("main_game", ["new_1"])
        elif button is self._gui[0]["middle_new_button"]:
            self._game.pop_state()
            self._game.push_state("main_game", ["new_2"])
        elif button is self._gui[0]["bottom_new_button"]:
            self._game.pop_state()
            self._game.push_state("main_game", ["new_3"])

    def load_button_func(self, button):
        if button is self._gui[0]["top_load_button"]:
            self._game.pop_state()
            self._game.push_state("main_game", ["load_1"])
        elif button is self._gui[0]["middle_load_button"]:
            self._game.pop_state()
            self._game.push_state("main_game", ["load_2"])
        elif button is self._gui[0]["bottom_load_button"]:
            self._game.pop_state()
            self._game.push_state("main_game", ["load_3"])

    def exit_click(self, button):
        self._game.pop_state()
