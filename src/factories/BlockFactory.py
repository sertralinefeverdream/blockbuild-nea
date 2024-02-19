from blocks.GenericBlock import GenericBlock
from blocks.DoorBlock import DoorBlock
from blocks.ChestBlock import ChestBlock
from blocks.RespawnAnchorBlock import RespawnAnchorBlock

#uploaded

class BlockFactory:
    def __init__(self, blocks_data):
        self._blocks_data = blocks_data

    def create_block(self, game, world, position, block_id, state_data=None):
        if block_id in self._blocks_data.keys():
            block_data = self._blocks_data[block_id]
            block = None
            if block_data["type"] == "generic":
                block = GenericBlock(game, world, position, block_data["hardness"], block_id,
                                     game.block_spritesheet.parse_sprite(block_data["texture"]),
                                     block_data["mine_sfx_id"], block_data["place_and_break_sfx_id"],
                                     block_data["footstep_sfx_id"], block_data["loot_drop_id"],
                                     block_data["loot_drop_tool_whitelist"], block_data["can_collide"])
            elif block_data["type"] == "door":
                block = DoorBlock(game, world, position, block_data["hardness"], block_id,
                                  game.block_spritesheet.parse_sprite(block_data["texture"]), block_data["mine_sfx_id"],
                                  block_data["place_and_break_sfx_id"], block_data["footstep_sfx_id"],
                                  block_data["use_sfx_id"], block_data["open_texture_id"],
                                  block_data["closed_texture_id"], block_data["loot_drop_id"],
                                  block_data["loot_drop_tool_whitelist"], block_data["can_collide"])
            elif block_data["type"] == "chest":
                block = ChestBlock(game, world, position, block_data["hardness"], block_id,
                                   game.block_spritesheet.parse_sprite(block_data["texture"]),
                                   block_data["mine_sfx_id"],
                                   block_data["place_and_break_sfx_id"], block_data["footstep_sfx_id"],
                                   block_data["use_sfx_id"], block_data["loot_drop_id"],
                                   block_data["loot_drop_tool_whitelist"], block_data["can_collide"])
            elif block_data["type"] == "respawn_anchor":
                block = RespawnAnchorBlock(game, world, position, block_data["hardness"], block_id,
                                           game.block_spritesheet.parse_sprite(block_data["texture"]),
                                           block_data["mine_sfx_id"],
                                           block_data["place_and_break_sfx_id"], block_data["footstep_sfx_id"],
                                           block_data["use_sfx_id"], block_data["loot_drop_id"],
                                           block_data["loot_drop_tool_whitelist"], block_data["can_collide"])
            else:
                raise NotImplementedError

            if state_data is not None:
                block.load_state_data(state_data)

            return block
