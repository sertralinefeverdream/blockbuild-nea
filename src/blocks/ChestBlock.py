from blocks.InteractableBlockBase import InteractableBlockBase

#uploaded

class ChestBlock(InteractableBlockBase):
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, use_sfx_id, loot_drop_id=None, loot_drop_tool_whitelist=None, can_collide=True):
        super().__init__(game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                         footstep_sfx_id, use_sfx_id, loot_drop_id, loot_drop_tool_whitelist, can_collide)

        self._container = self._game.item_container_factory.create_item_container("item_container", self._game,
                                                                                  self._world, 6, 6)

    def interact(self):
        self._game.sfx_handler.play_sfx(self._use_sfx_id, self._game.get_option("game_volume").value)
        self._game.push_state("chest_interact",
                              [self._world.player.inventory, self._world.player.hotbar, self._container])
        pass

    def get_state_data(self):
        data = {}
        data["container_state_data"] = self._container.get_state_data()
        return data

    def load_state_data(self, data):
        self._container.load_from_data(data["container_state_data"])
