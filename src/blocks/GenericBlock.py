from src.blocks.BlockBase import BlockBase


class GenericBlock(BlockBase):
    def __init__(self, game, block_id, sfx_handler, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        super().__init__(game, block_id, sfx_handler, texture, break_sfx_id, place_sfx_id, footstep_sfx_id)

    def init_audio(self):
        self._sfx_handler.add_sfx_from_dict(
            {
                self._break_sfx_id: self._game.config["sfx_assets"][self._break_sfx_id],
                self._place_sfx_id: self._game.config["sfx_assets"][self._place_sfx_id],
                self._footstep_sfx_id: self._game.config["sfx_assets"][self._footstep_sfx_id]
            }
        )

    def update(self):
        print("Hurray!")

    def draw(self, screen_position):
        print(screen_position)
        self._game.window.blit(self._texture, screen_position)

    def get_state_data(self):
        return None



