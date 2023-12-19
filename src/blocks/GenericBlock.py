from src.blocks.BlockBase import BlockBase
import json


class GenericBlock(BlockBase):
    def __init__(self, game, block_id, sfx_handler, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        super().__init__(game, block_id, sfx_handler, texture, break_sfx_id, place_sfx_id, footstep_sfx_id)

    def init_audio(self):
        pass

    def update(self):
        print("Hurray!")

    def draw(self, screen_position):
        self._game.window.blit(self._texture, screen_position)

    def serialize(self):
        data = \
        {
            "block_id": f"{self._block_id}",
            "state_data": None
        }
        return json.dumps(data)
