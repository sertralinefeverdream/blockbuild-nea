from abc import ABC, abstractmethod

from blocks.GenericBlock import GenericBlock

#uploaded

class InteractableBlockBase(GenericBlock):
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, use_sfx_id, loot_drop_id=None, loot_drop_tool_whitelist=None, can_collide=True):
        super().__init__(game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                         footstep_sfx_id, loot_drop_id, loot_drop_tool_whitelist, can_collide)
        self._use_sfx_id = use_sfx_id

    @abstractmethod
    def interact(self):
        pass
