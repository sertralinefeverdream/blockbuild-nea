from items.GenericItem import GenericItem
from items.BlockItem import BlockItem
from items.ToolItem import ToolItem
from items.FoodItem import FoodItem

#uploaded

class ItemFactory:
    def __init__(self, items_data):
        self._items_data = items_data

    def create_item(self, game, world, item_id, state_data=None, quantity_override=None):
        if item_id in self._items_data.keys():
            item_data = self._items_data[item_id]
            item = None
            if item_data["type"] == "generic":
                item = GenericItem(game, world, item_id, item_data["name"],
                                   game.item_spritesheet.parse_sprite(item_data["texture"]),
                                   max_quantity=item_data["max_quantity"], attack_cooldown=item_data["attack_cooldown"],
                                   use_cooldown=item_data["use_cooldown"], attack_range=item_data["attack_range"],
                                   use_range=item_data["use_range"], attack_strength=item_data["attack_strength"],
                                   default_mine_strength=item_data["default_mine_strength"],
                                   preferred_mine_strength=item_data["preferred_mine_strength"],
                                   preferred_mine_strength_white_list=item_data["preferred_mine_strength_whitelist"])
            elif item_data["type"] == "blockitem":
                item = BlockItem(game, world, item_id, item_data["name"],
                                 game.block_spritesheet.parse_sprite(item_data["texture"]),
                                 max_quantity=item_data["max_quantity"], attack_cooldown=item_data["attack_cooldown"],
                                 use_cooldown=item_data["use_cooldown"], attack_range=item_data["attack_range"],
                                 use_range=item_data["use_range"], attack_strength=item_data["attack_strength"],
                                 default_mine_strength=item_data["default_mine_strength"],
                                 preferred_mine_strength=item_data["preferred_mine_strength"],
                                 preferred_mine_strength_white_list=item_data["preferred_mine_strength_whitelist"],
                                 block_id=item_data["block_id"])
            elif item_data["type"] == "tool":
                item = ToolItem(game, world, item_id, item_data["name"],
                                game.item_spritesheet.parse_sprite(item_data["texture"]),
                                tool_break_sfx_id=item_data["tool_break_sfx_id"],
                                max_quantity=item_data["max_quantity"], attack_cooldown=item_data["attack_cooldown"],
                                use_cooldown=item_data["use_cooldown"], attack_range=item_data["attack_range"],
                                use_range=item_data["use_range"], attack_strength=item_data["attack_strength"],
                                default_mine_strength=item_data["default_mine_strength"],
                                preferred_mine_strength=item_data["preferred_mine_strength"],
                                preferred_mine_strength_white_list=item_data["preferred_mine_strength_whitelist"],
                                durability=item_data["durability"])
            elif item_data["type"] == "food":
                item = FoodItem(game, world, item_id, item_data["name"],
                                game.item_spritesheet.parse_sprite(item_data["texture"]),
                                max_quantity=item_data["max_quantity"], attack_cooldown=item_data["attack_cooldown"],
                                use_cooldown=item_data["use_cooldown"], attack_range=item_data["attack_range"],
                                use_range=item_data["use_range"], attack_strength=item_data["attack_strength"],
                                default_mine_strength=item_data["default_mine_strength"],
                                preferred_mine_strength=item_data["preferred_mine_strength"],
                                preferred_mine_strength_white_list=item_data["preferred_mine_strength_whitelist"],
                                nutrition=item_data["nutrition"], eat_sfx_id=item_data["eat_sfx_id"]
                                )

            if state_data is not None:
                item.load_state_data(state_data)
            if quantity_override is not None:
                item.quantity = quantity_override
            return item
