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
                item = GenericItem(game, world, item_id, item_data["name"], self._item_spritesheet.parse_sprite(item_data["texture"]), max_quantity=item_data["max_quantity"], left_use_cooldown=item_data["left_use_cooldown"], right_use_cooldown=item_data["right_use_cooldown"], left_use_range=item_data["left_use_range"], right_use_range=item_data["right_use_range"])
                if state_data is not None:
                    item.left_use_timer = state_data["left_use_timer"]
                    item.right_use_timer = state_data["right_use_timer"]
                    item.quantity = state_data["quantity"]
                return item
            elif item_data["type"] == "blockitem":
                item = BlockItem(game, world, item_id, item_data["name"], self._block_spritesheet.parse_sprite(item_data["texture"]), max_quantity=item_data["max_quantity"], left_use_cooldown=item_data["left_use_cooldown"], right_use_cooldown=item_data["right_use_cooldown"], left_use_range=item_data["left_use_range"], right_use_range=item_data["right_use_range"], block_id=item_data["block_id"])
                print(f'''DUN! {item_data["right_use_range"]}''')
                if state_data is not None:
                    item.left_use_timer = state_data["left_use_timer"]
                    item.right_use_timer = state_data["right_use_timer"]
                    item.quantity = state_data["quantity"]
                return item