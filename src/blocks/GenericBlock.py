from src.blocks.BlockBase import BlockBase


class GenericBlock(BlockBase):
    def __init__(self, game, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        super().__init__(game, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id)

    def update(self):
        pass

    def draw(self, screen_position):
        self._game.window.blit(self._texture, screen_position)

    def get_state_data(self):
        return None



