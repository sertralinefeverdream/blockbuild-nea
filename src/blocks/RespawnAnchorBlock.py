from blocks.InteractableBlockBase import InteractableBlockBase

#uploaded

class RespawnAnchorBlock(InteractableBlockBase):
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, use_sfx_id, loot_drop_id=None, loot_drop_tool_whitelist=None, can_collide=True):
        super().__init__(game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                         footstep_sfx_id, use_sfx_id, loot_drop_id, loot_drop_tool_whitelist, can_collide)

    def interact(self):
        if not self._is_broken:
            self._game.sfx_handler.play_sfx(self._use_sfx_id, self._game.get_option("game_volume").value)
            self._world.respawn_location = self._position
            self.kill()
