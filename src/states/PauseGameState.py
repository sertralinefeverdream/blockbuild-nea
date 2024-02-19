import pygame
from states.StateBase import StateBase

#uploaded

class PauseGameState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._escape_key_held = False

    def initialise_gui(self):
        self._gui = [
            {
                "options_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                    self.options_button_click, text="Options"),
                "exit_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                 self.exit_button_click,
                                                                 text="Save & Exit")

            },
            {},
            {},
        ]

    def on_state_enter(self, params=None):
        self._game.music_handler.set_shuffle_list(["Atmos Sphear", "Aquatic Ambience"])
        if self._game.previous_state is not self._game.states["main_game"]:
            self._game.music_handler.shuffle_play()

        self._gui[0]["options_button"].size = (400.0, 75.0)
        self._gui[0]["options_button"].font_size = 45
        self._gui[0]["options_button"].centre_position = (600.0, 300.0)

        self._gui[0]["exit_button"].size = (400.0, 75.0)
        self._gui[0]["exit_button"].font_size = 45
        self._gui[0]["exit_button"].centre_position = (600.0, 500.0)

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def on_state_leave(self, params=None):
        pass

    def update(self):
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()

        if self._game.keys_pressed[pygame.K_ESCAPE]:
            self._escape_key_held = True
        elif not self._game.keys_pressed[pygame.K_ESCAPE] and self._escape_key_held:
            self._game.pop_state()
            self._escape_key_held = False

    def draw(self, no_gui=False):
        self._game.states["main_game"].draw(True)
        if not no_gui:
            for layer in self._gui[::-1]:
                for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                    component.draw()

    def options_button_click(self, button):
        self._game.push_state("options_menu")

    def exit_button_click(self, button):
        self._game.pop_state()  # Down to main game state
        self._game.pop_state([], ["save"])  # Down to load game state
