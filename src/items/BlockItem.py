import pygame
from src.items.GenericItem import GenericItem

class BlockItem(GenericItem):
    def __init__(self, game, world, name, texture, quantity=1, max_quantity=100, can_be_stacked=True, left_use_cooldown=100, right_use_cooldown=100, block_id="grass")
        super().__init__(game, world, name, texture, quantity, max_quantity, can_be_stacked, left_use_cooldown, right_use_cooldown)
        self._block_id = "grass"

    def right_use(self):
        mouse_pos = pygame.mouse.get_pos()
        world_pos_from_mouse = self._world.camera.get_world_position(mouse_pos)
        block_at_pos = self._world.get_block_at_position(world_pos_from_mouse)
        if block_at_pos is None and self._quantity > 0:
            self._quantity -= 1
            self._world.set_block_at_position(world_pos_from_mouse, self._block_id)


