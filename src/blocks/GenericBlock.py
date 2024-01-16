import pygame
from src.blocks.BlockBase import BlockBase


class GenericBlock(BlockBase):
    def __init__(self, game, world, position, hardness, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        super().__init__(game, world, position, hardness, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id)

    def update(self):
        screen_position = self._world.camera.get_screen_position(self._position)
        self._hitbox.update(screen_position, (40, 40))

    def get_state_data(self):
        return None



