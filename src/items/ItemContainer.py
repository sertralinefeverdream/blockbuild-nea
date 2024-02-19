#uploaded

class ItemContainer:
    def __init__(self, game, world, rows, columns):
        self._data = [[None for x in range(columns)] for row_index in range(rows)]  # Static size
        self._game = game
        self._world = world
        self._dimensions = (rows, columns)

    @property
    def data(self):
        return self._data

    def update(self):
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is not None:
                    if item.quantity == 0:
                        self._data[row_index][item_index] = None

    def reset(self):
        self._data.clear()
        self._data = [[None for x in range(self._dimensions[1])] for row_index in
                      range(self._dimensions[0])]

    def set_item_at_index(self, row, column, item=None):
        self._data[row][column] = item

    def get_item_indexes(self, item):
        for row_index, row in enumerate(self._data):
            if item in row:
                return row_index, row.index(item)
        return -1, -1

    def get_item_at_index(self, row, column):
        return self._data[row][column]

    def has_items_of_quantity(self, item_id,
                              quantity=1):  # Do you have n or more of item of type "item_id" in this item container?
        total_quantity = self.get_total_quantity_by_id(item_id)
        return total_quantity >= quantity

    def get_total_quantity_by_id(self,
                                 item_id):  # Get how many of this item of type item_id you have in your item container total
        list_of_items_of_same_type = self.get_items_of_same_type_by_id(item_id)
        return sum([item.quantity for item in list_of_items_of_same_type])

    def deplete_item(self, item_id, amount_to_deplete):
        if self.get_total_quantity_by_id(item_id) > 0:
            print("CASE 1: There is at least one of this item type in the item container")
            list_of_items = self.get_items_of_same_type_by_id(item_id)
            list_of_items.sort(key=lambda l: l.quantity)
            total_depleted = 0
            for item in list_of_items:
                if item.quantity > 0:
                    for x in range(item.quantity):
                        item.quantity -= 1
                        total_depleted += 1
                        if total_depleted == amount_to_deplete:
                            return 0
                        if item.quantity == 0:
                            break
                    else:
                        print("ITEM QUANTITY IS 0")

            return amount_to_deplete - total_depleted  # Return remainder left to deplete

        else:
            return amount_to_deplete
            print("CASE 2: There is 0 of this item type in the item container")

    def pickup_item(self, item_to_pickup, capacity_check=False):
        if capacity_check and self.get_remaining_capacity_of_same_type_by_object(
                item_to_pickup) < item_to_pickup.quantity:
            print("NOT ENOUGH SPACE")
            return item_to_pickup

        unfilled_items_list = self.get_unfilled_items_of_same_type_by_object(item_to_pickup)
        if len(unfilled_items_list) > 0:
            item_with_highest_quantity = unfilled_items_list[0]
            for item in unfilled_items_list:
                if item.quantity > item_with_highest_quantity.quantity:
                    item_with_highest_quantity = item
            remaining_quantity = item_with_highest_quantity.max_quantity - item_with_highest_quantity.quantity
            if item_to_pickup.quantity > remaining_quantity:
                item_with_highest_quantity.quantity += remaining_quantity
                item_to_pickup.quantity -= remaining_quantity
                return self.pickup_item(item_to_pickup, capacity_check)
            elif item_to_pickup.quantity <= remaining_quantity:
                item_with_highest_quantity.quantity += item_to_pickup.quantity
                item_to_pickup.quantity = 0
                return None
        elif self.empty_item_exists():
            row_index, item_index = self.get_empty_item_indexes()[0]
            self._data[row_index][item_index] = item_to_pickup
            return None
        else:
            return item_to_pickup

    def get_remaining_capacity_of_same_type_by_object(self,
                                                      item_to_check):  # How many more of item_to_check could you fit in this item container?
        total = 0
        list_of_same_items = self.get_unfilled_items_of_same_type_by_object(item_to_check)
        print(list_of_same_items, "THIS TOO!!!!")
        for item in list_of_same_items:
            total += (item.max_quantity - item.quantity)

        for empty_slot in self.get_empty_item_indexes():
            total += item_to_check.max_quantity

        return total

    def get_remaining_capacity_of_same_type_by_id(self, item_id):
        total = 0
        list_of_same_items = self.get_unfilled_items_of_same_type_by_id(item_id)
        for item in list_of_same_items:
            total += (item.max_quantity - item.quantity)

        for empty_slot in self.get_empty_item_indexes():
            total += self._game.config["items"][item_id]["max_quantity"]

        return total

    def get_empty_item_indexes(self):
        indexes = []
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is None:
                    indexes.append((row_index, item_index))
        return indexes

    def empty_item_exists(self):
        for row in self._data:
            for item in row:
                if item is None:
                    return True
        return False

    def get_items_of_same_type_by_object(self, item_to_check):
        return self.get_items_of_same_type_by_id(item_to_check.item_id)

    def get_items_of_same_type_by_id(self, item_id):
        items_list = []
        for row in self._data:
            for item in row:
                if item is not None:
                    if item.item_id == item_id:
                        items_list.append(item)
        return items_list

    def get_unfilled_items_of_same_type_by_id(self, item_id):
        return [item for item in self.get_items_of_same_type_by_id(item_id) if item.quantity < item.max_quantity]

    def get_unfilled_items_of_same_type_by_object(self, item_to_check):

        # legacy code
        # unfilled_items_list = []
        # for row in self._data:
        #   for item in row:
        #      if item is not None:
        #         if item.item_id == item_to_check.item_id and item.quantity < item.max_quantity:
        #            print("Unfilled item added for return")
        #           unfilled_items_list.append(item)
        # return unfilled_items_list
        return [item for item in self.get_items_of_same_type_by_object(item_to_check) if
                item.quantity < item.max_quantity]

    def convert_data(self):
        data = \
            {
                "container_id": "item_container",
                "state_data": self.get_state_data()
            }
        return data

    # ItemContainer class save and load methods
    def load_from_data(self, data):
        self._data.clear()
        # print(f"data:{self._data}")
        self._dimensions = (len(data), len(data[0]))
        self._data = [[None for column_index in range(self._dimensions[1])] for row_index in range(self._dimensions[0])]

        for row_index, row in enumerate(data):
            self._data.append([])
            for item_index, item in enumerate(row):
                if item is not None:
                    self._data[row_index][item_index] = self._game.item_factory.create_item(self._game, self._world,
                                                                                            item["item_id"],
                                                                                            item["state_data"])
                else:
                    self._data[row_index][item_index] = None

    def get_state_data(self):
        data = [[None for x in range(self._dimensions[1])] for y in range(self._dimensions[0])]
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is not None:
                    data[row_index][item_index] = item.convert_data()
                else:
                    data[row_index][item_index] = None
        return data
