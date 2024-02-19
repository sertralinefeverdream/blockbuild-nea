from items.ItemContainer import ItemContainer

#uploaded

class HotbarContainer(ItemContainer):
    def __init__(self, game, world, columns):
        super().__init__(game, world, 1, columns)
        self._current_item_pointer = 0
        self._no_hands_item = self._game.item_factory.create_item(self._game, self._world, "empty_hands")
        self._current_item = self._no_hands_item

    @property
    def current_item_pointer(self):
        return self._current_item_pointer

    @current_item_pointer.setter
    def current_item_pointer(self, value):
        if 0 <= value <= self._dimensions[1] and value != self._current_item_pointer:
            self._current_item.on_unequip()
            self._current_item_pointer = value
            self.update_current_item()
            self._current_item.on_equip()

    @property
    def current_item(self):
        return self._current_item

    def update(self, player_centre_pos=None, update_current_item=True):
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is not None:
                    if item.quantity == 0:
                        self._data[row_index][item_index] = None

        if update_current_item and player_centre_pos is not None:
            self.update_current_item()
            if self._current_item is not None:
                return self._current_item.update(player_centre_pos)

    def update_current_item(self):
        if self._data[0][self._current_item_pointer] is not None:
            self._current_item = self._data[0][self._current_item_pointer]
        else:
            self._current_item = self._no_hands_item
