from src.blocks.GenericBlock import GenericBlock

class BlockFactory:
    def __init__(self, blocks_data):
        self._blocks_data = blocks_data

    def create_block(self, game, world, position, block_id, state_data=None):
        if block_id in self._blocks_data.keys():
            block_data = self._blocks_data[block_id]
            if block_data["type"] == "generic":
                return GenericBlock(game, world, position, block_data["hardness"], block_id, game.block_spritesheet.parse_sprite(block_data["texture"]), block_data["mine_sfx_id"], block_data["place_and_break_sfx_id"], block_data["footstep_sfx_id"], block_data["loot_drop_id"], block_data["loot_drop_tool_whitelist"], block_data["can_collide"])
            else:
                raise NotImplementedError

