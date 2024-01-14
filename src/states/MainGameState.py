import pygame
from src.states.StateBase import StateBase


class MainGameState(StateBase):
    def __init__(self, game, world):
        super().__init__(game)
        self._world = world
        self._escape_key_held = False

    def initialise_gui(self):
        self._gui = [
            {"fps_counter": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window, text="default")},
            {"block_box":self._game.gui_factory.create_gui("RectBox", self._game, self._game.window, size=(40.0, 40.0), outline_thickness=3, has_box=False)},
            {}
        ]

    def on_state_enter(self, params=None):
        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

        if params is not None:
            if params[0] == "load":
                print("load")
            elif params[0] == "new":
                print("new")

    def on_state_leave(self, params=None):
        if params is not None:
            if params[0] == "save":
                print("saving")

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self._world.update()
        self._gui[0]["fps_counter"].text = str(self._game.clock.get_fps()//1)

        block_at_mouse = self._world.get_block_at_position(self._world.camera.get_world_position(mouse_pos))

        if block_at_mouse is not None:
            self._gui[1]["block_box"].is_visible = True
            self._gui[1]["block_box"].position = self._world.camera.get_screen_position(block_at_mouse.position)
        else:
            self._gui[1]["block_box"].is_visible = False
            print("Invisible")

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

        if self._game.keys_pressed[pygame.K_ESCAPE]:
            self._escape_key_held = True
        elif not self._game.keys_pressed[pygame.K_ESCAPE] and self._escape_key_held:
            self._game.push_state("pause_game")
            self._escape_key_held = False

    def draw(self, no_gui=False):
        self._world.draw()
        if not no_gui:
            for layer in self._gui[::-1]:
                for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                    component.draw()

