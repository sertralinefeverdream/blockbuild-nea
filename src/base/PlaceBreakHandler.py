import pygame.mouse

class PlaceBreakHandler:
    def __init__(self, game, world):
        self._game = game
        self._world = world

        self._current_block_hovering = None
        self._previous_block_hovering = None
        self._block_equipped = "grass"

    @property
    def current_block_hovering(self):
        return self._current_block_hovering

    def update(self):
        left_key_pressed = pygame.mouse.get_pressed()[0]
        right_key_pressed = pygame.mouse.get_pressed()[2]
        mouse_world_pos = self._world.camera.get_world_position(pygame.mouse.get_pos())

        self._previous_block_hovering = self._current_block_hovering
        self._current_block_hovering = self._world.get_block_at_position(mouse_world_pos)

        if left_key_pressed:
            self.break_block(mouse_world_pos)
        elif right_key_pressed:
            self.place_block(mouse_world_pos)

    def place_block(self, world_pos):
        if self._current_block_hovering is None:
            print("Yes!")
            self._world.set_block_at_position(world_pos, self._block_equipped)
            self._world.get_block_at_position(world_pos).on_place()

    def break_block(self, world_pos):
        if self._current_block_hovering is not None:
            pass
