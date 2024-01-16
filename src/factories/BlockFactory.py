from src.blocks.GenericBlock import GenericBlock

class BlockFactory:
    def __init__(self, blocks_data, sprite_sheet):
        self._blocks_data = blocks_data
        self._sprite_sheet = sprite_sheet

    def create_block(self, game, world, position, block_id, state_data=None):
        if block_id in self._blocks_data.keys():
            block_data = self._blocks_data[block_id]
            if block_data["type"] == "generic":
                #Generic block type has not state data by default
                return GenericBlock(game, world, position, block_id, self._sprite_sheet.parse_sprite(block_data["texture"]), block_data["break_sfx_id"], block_data["place_sfx_id"], block_data["footstep_sfx_id"])
            else:
                raise NotImplementedError

