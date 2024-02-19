from blocks.BlockBase import BlockBase

#uploaded

class GenericBlock(BlockBase):
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, loot_drop_id=None, loot_drop_tool_whitelist=None, can_collide=True):
        super().__init__(game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                         footstep_sfx_id, loot_drop_id, loot_drop_tool_whitelist, can_collide)

    def update(self):
        screen_position = self._world.camera.get_screen_position(self._position)
        self._hitbox.update(screen_position, (40, 40))

    def get_state_data(self):
        return None

    def load_state_data(self, data):
        pass  # GenericBlock type has no state data so it doesnt really matter
