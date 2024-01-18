from src.items.ItemContainer import ItemContainer

class HotbarContainer(ItemContainer):
    def __init__(self, game, world, columns):
        super().__init__(game, world, 1, columns)
        self._current_item_pointer = 0
        self._no_hands_item = self._game.item_factory.create_item(self._game, self._world, "grass_block")
        self._current_item = self._no_hands_item

    @property
    def current_item(self):
        return self._current_item

    @property
    def current_item_pointer(self):
        return self._current_item_pointer

    @current_item_pointer.setter
    def current_item_pointer(self, value):
        if 0 <= value <= self._dimensions[1]:
            self._current_item_pointer = value
            self.update_current_item()

    def update_current_item(self):
        if self._data[0][self._current_item_pointer] is not None:
            self._current_item = self._data[0][self._current_item_pointer]
        else:
            self._current_item = self._no_hands_item

    def update(self, player_pos):
        print("updating")
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is not None:
                    if item.quantity == 0:
                        self._data[row_index][item_index] = None

        self.update_current_item()
        if self._current_item is not None:
            self._current_item.update(player_pos)




