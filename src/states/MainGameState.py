import pygame.mouse

from src.states.StateBase import StateBase


class MainGameState(StateBase):
    def __init__(self, game, world):
        super().__init__(game)
        self._world = world
        self._escape_key_held = False
        self._save_file_pointer = None

    def initialise_gui(self):
        self._gui = [
            {"fps_counter": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window, text="default")},
            {"block_border": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window, size=(40.0, 40.0),
                                                            outline_thickness=3, has_box=False),
            "block_health_bar": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window, size=(40.0, 10.0), has_outline=False, box_colour=(190, 190, 190))},
            {}
        ]

    def on_state_enter(self, params=None):
        self._gui[0]["fps_counter"].position = (12.5, 12.5)
#        self._gui[0]["hotbar_0"].position = (300, 700)

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

        if params is not None:
            if params[0] == "load_1":
                self._world.reset()
                self._save_file_pointer = "save_file_1"
                self._game.file_save_handler.load_world(self._world, "save_file_1")
            elif params[0] == "load_2":
                self._world.reset()
                self._save_file_pointer = "save_file_2"
                self._game.file_save_handler.load_world(self._world, "save_file_2")
            elif params[0] == "load_3":
                self._world.reset()
                self._save_file_pointer = "save_file_3"
                self._game.file_save_handler.load_world(self._world, "save_file_3")
            elif params[0] == "new_1":
                self._world.reset()
                self._save_file_pointer = "save_file_1"
            elif params[0] == "new_2":
                self._world.reset()
                self._save_file_pointer = "save_file_2"
            elif params[0] == "new_3":
                self._world.reset()
                self._save_file_pointer = "save_file_3"


    def on_state_leave(self, params=None):
        if params is not None:
            if params[0] == "save":
                self._game.file_save_handler.save_world(self._world, self._save_file_pointer)
                print("SAVING!!")

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self._world.update()

        self._gui[0]["fps_counter"].text = str(self._game.clock.get_fps()//1)
        self._gui[0]["fps_counter"].is_visible = False
        #self._gui[0]["hotbar_0"].item = self._world.player.hotbar[0]

        block_at_mouse = self._world.get_block_at_position(self._world.camera.get_world_position(mouse_pos))

        if block_at_mouse is not None:
            self._gui[1]["block_border"].is_visible = True
            self._gui[1]["block_border"].position = self._world.camera.get_screen_position(block_at_mouse.position)
        else:
            self._gui[1]["block_border"].is_visible = False


        current_player_tool = self._world.player.hotbar.current_item
        if current_player_tool is not None:
            if current_player_tool.is_mining:
                self._gui[1]["block_health_bar"].is_visible = True
                self._gui[1]["block_health_bar"].size[0] = (current_player_tool.block_currently_hovering_hardness_remaining/current_player_tool.block_currently_hovering.hardness) * 30
                self._gui[1]["block_health_bar"].centre_position = current_player_tool.block_currently_hovering.hitbox.center
            else:
                self._gui[1]["block_health_bar"].is_visible = False
        else:
            self._gui[1]["block_health_bar"].is_visible = False



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
                for component in layer.values():
                    component.draw()

