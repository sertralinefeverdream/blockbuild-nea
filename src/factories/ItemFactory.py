from src.items.GenericItem import GenericItem
from src.items.BlockItem import BlockItem

class ItemFactory:
    def __init__(self, items_data, item_spritesheet, block_spritesheet):
        self._items_data = items_data
        self._item_spritesheet = item_spritesheet
        self._block_spritesheet = block_spritesheet

    def create_item(self, game, world, item_id, state_data=None):
        if item_id in self._items_data.keys():
            item_data = self._items_data[item_id]
            if item_data["type"] == "generic":
                item = GenericItem(game, world, item_id, item_data["name"], self._item_spritesheet.parse_sprite(item_data["texture"]), max_quantity=item_data["max_quantity"], attack_cooldown=item_data["attack_cooldown"], use_cooldown=item_data["use_cooldown"], attack_range=item_data["attack_range"], use_range=item_data["use_range"], attack_strength=item_data["attack_strength"], default_mine_strength=item_data["default_mine_strength"], preferred_mine_strength=item_data["preferred_mine_strength"], preferred_mine_strength_white_list=item_data["preferred_mine_strength_whitelist"])
                if state_data is not None:
                    item.attack_timer = state_data["attack_timer"]
                    item.use_timer = state_data["use_timer"]
                    item.quantity = state_data["quantity"]
                return item
            elif item_data["type"] == "blockitem":
                item = BlockItem(game, world, item_id, item_data["name"], self._block_spritesheet.parse_sprite(item_data["texture"]), max_quantity=item_data["max_quantity"], attack_cooldown=item_data["attack_cooldown"], use_cooldown=item_data["use_cooldown"], attack_range=item_data["attack_range"], use_range=item_data["use_range"], attack_strength=item_data["attack_strength"], default_mine_strength=item_data["default_mine_strength"], preferred_mine_strength=item_data["preferred_mine_strength"], preferred_mine_strength_white_list=item_data["preferred_mine_strength_whitelist"], block_id=item_data["block_id"])
                print(f'''DUN! {item_data["use_range"]}''')
                if state_data is not None:
                    item.attack_timer = state_data["attack_timer"]
                    item.use_timer = state_data["use_timer"]
                    item.quantity = state_data["quantity"]
                return item