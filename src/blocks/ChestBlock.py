from src.blocks.InteractableBlockBase import InteractableBlockBase

class Chest(InteractableBlockBase)
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, use_sfx_id, loot_drop_id=None, loot_drop_tool_whitelist=None, can_collide=True):
        super().__init__(game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                         footstep_sfx_id, use_sfx_id, loot_drop_id, loot_drop_tool_whitelist)

        self._container = self._game.container.item_container_factory.create_item_container("item_container")


    def interact(self):
        pass

    def get_state_data(self):
        data = {}
        data["container_state_data"] = self._container.get_state_data()
        return data

    def load_state_data(self, data):
        self._container.load_from_data(data["container_state_data"])