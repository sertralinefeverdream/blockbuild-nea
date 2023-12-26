import pygame
from src.blocks.BlockBase import BlockBase


class GenericBlock(BlockBase):
    def __init__(self, game, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        super().__init__(game, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id)

    def update(self):
        pass

    def draw(self, screen_position):
        print("YES")
        self._hitbox.update(screen_position, (40, 40))
        self._game.window.blit(self._texture, screen_position)
        pygame.draw.rect(self._game.window, (0, 0, 0), self._hitbox, -1) # Draws hitbox

    def get_state_data(self):
        return None



