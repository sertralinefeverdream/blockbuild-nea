from src.states.StateBase import StateBase


class LoadGameMenuState(StateBase):
    def __init__(self, game, GUIFactory, AudioHandlerFactory):
        super().__init__(game, GUIFactory, AudioHandlerFactory)

    def initialise_gui(self):
        self._gui = [
            {
                "top_save_label": self._GUIFactory.create_gui("TextLabel", self._game, self._game.window, text="Save 1:"),
                "top_load_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.load_button_func, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Load"),
                "top_new_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.new_button_func, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="New"),

                "middle_save_label": self._GUIFactory.create_gui("TextLabel", self._game, self._game.window, text="Save 2:"),
                "middle_load_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.load_button_func, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Load"),
                "middle_new_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.new_button_func, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="New"),

                "bottom_save_label": self._GUIFactory.create_gui("TextLabel", self._game, self._game.window, text="Save 3:"),
                "bottom_load_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.load_button_func, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Load"),
                "bottom_new_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.new_button_func, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="New"),
                
                "exit_button": self._GUIFactory.create_gui("TextButton", self._game, self._game.window, self.exit_click, self._AudioHandlerFactory.create_handler("SfxHandler", self._game), text="Exit")
            },
            {},
            {
                "top_box":self._GUIFactory.create_gui("RectBox", self._game, self._game.window),
                "middle_box": self._GUIFactory.create_gui("RectBox", self._game, self._game.window),
                "bottom_box": self._GUIFactory.create_gui("RectBox", self._game, self._game.window)

             }
        ]

    def on_state_enter(self, *args):
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

    def new_button_func(self, button):
        if button is self._gui[0]["top_new_button"]:
            print("New Top")
        elif button is self._gui[0]["middle_new_button"]:
            print("New Middle")
        elif button is self._gui[0]["bottom_new_button"]:
            print("New Bottom")

    def load_button_func(self, button):
        if button is self._gui[0]["top_load_button"]:
            print("Load Top")
        elif button is self._gui[0]["middle_load_button"]:
            print("Load Middle")
        elif button is self._gui[0]["bottom_load_button"]:
            print("Load Bottom")

    def on_state_leave(self):
        pass

    def update(self):
        self._game.window.fill((255, 255, 255))
        for layer in self._gui[::-1]:  # Iterates through all guis in dict and updates and draws them
            for component in layer.values():
                component.update()
                component.draw()

    def exit_click(self, button):
        self._game.pop_state()
