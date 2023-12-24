from src.states.StateBase import StateBase
import pygame

class MainGameState(StateBase):
    def __init__(self, game, world, place_break_handler):
        super().__init__(game)
        self._world = world
        self._place_break_handler = place_break_handler

    def initialise_gui(self):
        self._gui = [
            {"block_marker": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window, size=(40.0, 40.0), outline_thickness=2, has_box=False)},
            {},
            {}
        ]

    def on_state_enter(self):
        pass

    def on_state_leave(self):
        pass

    def update_block_marker(self):
        if self._place_break_handler.current_block_hovering is None:
            self._gui[0]["block_marker"].is_visible = False
        else:
            self._gui[0]["block_marker"].is_visible = True

            world_pos_x, world_pos_y = self._world.camera.get_world_position(pygame.mouse.get_pos())
            block_pos_x, block_pos_y = (world_pos_x // 40 * 40, world_pos_y // 40 * 40)
            screen_pos_x, screen_pos_y = self._world.camera.get_screen_position((block_pos_x, block_pos_y))
            self._gui[0]["block_marker"].position = (screen_pos_x, screen_pos_y)

    def update(self):
        self._game.window.fill((255, 255, 255))
      #  self._world.camera.x += 50 / self._game.clock.get_time()
      #  self._world.camera.y += 50 / self._game.clock.get_time()
        self._place_break_handler.update()
        self._world.update()

        self.update_block_marker()
        self._world.draw()
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()
