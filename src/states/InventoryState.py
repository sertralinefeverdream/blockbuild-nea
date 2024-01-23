from src.states.StateBase import StateBase
import pygame


class InventoryState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._inventory = None
        self._hotbar = None
        self._inventory_key_held = False
        self._item_selected = None  # In the form (row_index, column_index, id) where id identifies whether the item originates from the inventory or the hotbar
        self._recipe_selected = None
        self._mode = "default"
        self._crafting_recipes = {}
        self._world = None

        for item_id, item_data in self._game.config["items"].items():
            if item_data["recipe"] is not None:
                self._crafting_recipes[item_id] = item_data["recipe"]

        print(self._crafting_recipes)

    def initialise_gui(self):
        self._gui = [
            {
                "inventory_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                       self._game.window, 9, 9,
                                                                       self.on_inventory_item_press),
                "hotbar_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                    self._game.window, 1, 9, self.on_hotbar_item_press),
                "move_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                 self.on_move_button_press),
                "delete_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                   self.on_delete_button_press),
                "merge_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                  self.on_merge_button_press),
                "craft_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                  self.on_craft_button_press),
                "item_description_box": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window),
                "test_pickaxe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                               self._game.window,
                                                                               self.on_craft_item_press)
            },
            {},
            {
                "crafting_background": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window),
                # "crafting_info_background": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window)
            }
        ]

    def on_craft_button_press(self, button):
        if self.check_can_craft(self._recipe_selected) and self._recipe_selected is not None:
            item = self._game.item_factory.create_item(self._game, self._world, self._recipe_selected,
                                                       quantity_override=self._crafting_recipes[self._recipe_selected][
                                                           "amount_crafted"])
            print(f"HERE IT IS {item}")
            if self._hotbar.get_remaining_capacity_of_same_type(
                    item) + self._inventory.get_remaining_capacity_of_same_type(item) > item.quantity:
                for ingredient_name, quantity_required in self._crafting_recipes[self._recipe_selected][
                    "ingredients"].items():
                    remainder = self._hotbar.deplete_item(ingredient_name, quantity_required)
                    if remainder > 0:
                        remainder = self._inventory.deplete_item(ingredient_name, remainder)
                    if remainder > 0:
                        print("THIS CASE SHOULD NOT BE REACHED!!")
                self._hotbar.update(None, False)
                self._inventory.update()
                pickup_remainder = self._hotbar.pickup_item(item)
                if pickup_remainder is not None:
                    pickup_remainder = self._inventory.pickup(pickup_remainder)
                if pickup_remainder is not None:
                    print("THIS CASE SHOULDNT BE REACHED EITHER")

    def check_can_craft(self, recipe_id):
        if recipe_id is not None:
            for ingredient_name, quantity_required in self._crafting_recipes[recipe_id]["ingredients"].items():
                if self._hotbar.get_total_quantity_by_id(ingredient_name) + self._inventory.get_total_quantity_by_id(
                        ingredient_name) < quantity_required:
                    return False
            return True
        else:
            return False

    def on_craft_item_press(self, item_button):
        self._mode = "default"
        self._item_selected = None
        if item_button is self._gui[0]["test_pickaxe_craft_button"]:
            self._recipe_selected = "test_pickaxe"

    def on_hotbar_item_press(self, item_button):
        self._recipe_selected = None

        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0][
                "hotbar_display"])
            if self._hotbar.get_item_at_index(item_button_row, item_button_column) is not None:
                self._item_selected = (item_button_row, item_button_column, "hotbar")
            else:
                self._item_selected = None
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0][
                "hotbar_display"])
            self.swap((item_button_row, item_button_column, "hotbar"), self._item_selected)
            self._item_selected = None
            self._mode = "default"
        elif self._mode == "merge":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0][
                "hotbar_display"])
            selected_item_container = self._inventory if self._item_selected[2] == "inventory" else self._hotbar
            item_1 = selected_item_container.get_item_at_index(self._item_selected[0], self._item_selected[1])
            item_2 = self._hotbar.get_item_at_index(item_button_row, item_button_column)
            if item_2 is not None:
                if item_1.item_id == item_2.item_id and item_1 is not item_2 and item_2.quantity < item_2.max_quantity:
                    self.merge(self._item_selected, (item_button_row, item_button_column, "hotbar"))
                    self._item_selected = None
                    self._mode = "default"

    def on_inventory_item_press(self, item_button):
        self._recipe_selected = None

        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0][
                "inventory_display"])
            if self._inventory.get_item_at_index(item_button_row, item_button_column) is not None:
                self._item_selected = (item_button_row, item_button_column, "inventory")
            else:
                self._item_selected = None
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0][
                "inventory_display"])
            self.swap((item_button_row, item_button_column, "inventory"), self._item_selected)
            self._item_selected = None
            self._mode = "default"
        elif self._mode == "merge":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0][
                "inventory_display"])
            selected_item_container = self._inventory if self._item_selected[2] == "inventory" else self._hotbar
            item_1 = selected_item_container.get_item_at_index(
                self._item_selected[0], self._item_selected[1])
            item_2 = self._inventory.get_item_at_index(item_button_row, item_button_column)  # MERGING INTO
            if item_2 is not None:
                if item_1.item_id == item_2.item_id and item_1 is not item_2 and item_2.quantity < item_2.max_quantity:
                    self.merge(self._item_selected, (item_button_row, item_button_column, "inventory"))
                    self._item_selected = None
                    self._mode = "default"

    def swap(self, item_tuple_1, item_tuple_2):
        item_container_1 = self._inventory if item_tuple_1[2] == "inventory" else self._hotbar
        item_container_2 = self._inventory if item_tuple_2[2] == "inventory" else self._hotbar
        temp = item_container_1.get_item_at_index(item_tuple_1[0], item_tuple_1[1])

        item_container_1.set_item_at_index(item_tuple_1[0], item_tuple_1[1],
                                           item_container_2.get_item_at_index(item_tuple_2[0], item_tuple_2[1]))
        item_container_2.set_item_at_index(item_tuple_2[0], item_tuple_2[1], temp)

    def merge(self, item_tuple_1, item_tuple_2):
        item_container_1 = self._inventory if item_tuple_1[2] == "inventory" else self._hotbar
        item_container_2 = self._inventory if item_tuple_2[2] == "inventory" else self._hotbar

        item_1 = item_container_1.get_item_at_index(item_tuple_1[0], item_tuple_1[1])
        item_2 = item_container_2.get_item_at_index(item_tuple_2[0], item_tuple_2[1])

        if item_1.item_id == item_2.item_id:
            if item_2.quantity < item_2.max_quantity:
                max_amount_mergable = item_2.max_quantity - item_2.quantity
                if item_1.quantity <= max_amount_mergable:
                    print("CASE 1 NOW")
                    item_2.quantity += item_1.quantity
                    item_container_1.set_item_at_index(item_tuple_1[0], item_tuple_1[1], None)
                elif item_1.quantity > max_amount_mergable:
                    print("CASE 2 NOW")
                    item_1.quantity -= max_amount_mergable
                    item_2.quantity = item_2.max_quantity

    def find_item_button_indexes_in_display(self, item_button, container_display):
        for row_index, row in enumerate(container_display.gui):
            if item_button in row:
                return row_index, row.index(item_button)
        return None

    def on_move_button_press(self, button):
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_check = self._inventory if self._item_selected[2] == "inventory" else self._hotbar
                if container_to_check.get_item_at_index(self._item_selected[0], self._item_selected[1]) is not None:
                    self._mode = "move"
        elif self._mode == "move":
            self._mode = "default"

    def on_delete_button_press(self, button):
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_delete_from = self._inventory if self._item_selected[2] == "inventory" else self._hotbar
                if container_to_delete_from.get_item_at_index(self._item_selected[0],
                                                              self._item_selected[1]) is not None:
                    container_to_delete_from.set_item_at_index(self._item_selected[0], self._item_selected[1], None)
                    self._item_selected = None

    def on_merge_button_press(self, button):
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_check = self._inventory if self._item_selected[2] == "inventory" else self._hotbar
                if container_to_check.get_item_at_index(self._item_selected[0], self._item_selected[1]) is not None:
                    self._mode = "merge"
        elif self._mode == "merge":
            self._mode = "default"

    def on_state_enter(self, params=None):

        self._gui[0]["inventory_display"].centre_position = (300.0, 300.0)
        self._gui[0]["hotbar_display"].centre_position = (600.0, 700.0)

        self._gui[0]["move_button"].size = (110.0, 50.0)
        self._gui[0]["move_button"].centre_position = (175.0, 600.0)

        self._gui[0]["delete_button"].size = (110.0, 50.0)
        self._gui[0]["delete_button"].centre_position = (300.0, 600.0)

        self._gui[0]["merge_button"].size = (110.0, 50.0)
        self._gui[0]["merge_button"].centre_position = (425.0, 600.0)

        self._gui[0]["craft_button"].size = (110.0, 50.0)
        self._gui[0]["craft_button"].centre_position = (630.0, 470.0)
        self._gui[0]["craft_button"].text = "Craft"

        self._gui[0]["item_description_box"].size = (200.0, 50.0)
        self._gui[0]["item_description_box"].font_size = 30
        self._gui[0]["item_description_box"].text = "TEST"
        self._gui[0]["item_description_box"].position = (710.0, 459.0)

        self._gui[2]["crafting_background"].colour = (125, 50, 0)
        self._gui[2]["crafting_background"].size = (600.0, 400.0)
        self._gui[2]["crafting_background"].box_colour = (200, 200, 200)
        self._gui[2]["crafting_background"].centre_position = (875.0, 230.0)

        self._gui[0]["test_pickaxe_craft_button"].size = (60.0, 60.0)
        self._gui[0]["test_pickaxe_craft_button"].image = self._game.item_spritesheet.parse_sprite("wooden_pickaxe")
        self._gui[0]["test_pickaxe_craft_button"].image_scale_multiplier = 0.9
        self._gui[0]["test_pickaxe_craft_button"].centre_position = (630.0, 80.0)

        self._inventory = params[0] if params is not None else None
        self._hotbar = params[1] if params is not None else None
        self._world = params[2] if params is not None else None
        self._inventory_key_held = False
        self._item_selected = None
        self._mode = "default"

        self._gui[0]["inventory_display"].container = self._inventory
        self._gui[0]["hotbar_display"].container = self._hotbar

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def on_state_leave(self, params=None):
        pass

    def update(self):
        if self._game.keys_pressed[pygame.K_e]:
            self._inventory_key_held = True
        elif not self._game.keys_pressed[pygame.K_e] and self._inventory_key_held:
            self._game.pop_state()
            self._inventory_key_held = False

        self._hotbar.update(None, False)
        self._inventory.update()

        if self._mode == "default":
            self._gui[0]["move_button"].text = "Move Item"
            self._gui[0]["merge_button"].text = "Merge"
            self._gui[0]["delete_button"].text = "Delete"
            if self._item_selected is None:
                self._gui[0]["move_button"].is_visible = False
                self._gui[0]["delete_button"].is_visible = False
                self._gui[0]["merge_button"].is_visible = False
            else:
                self._gui[0]["move_button"].is_visible = True
                self._gui[0]["delete_button"].is_visible = True
                self._gui[0]["merge_button"].is_visible = True

            if self._recipe_selected is None:
                self._gui[0]["craft_button"].is_visible = False
                self._gui[0]["item_description_box"].is_visible = False
            else:
                self._gui[0]["craft_button"].is_visible = True
                self._gui[0]["item_description_box"].is_visible = True
                self._gui[0]["item_description_box"].text = self._crafting_recipes[self._recipe_selected]["description"]
                # self._gui[0]["item_description_box"].position = (850.0, 480.0)

        elif self._mode == "move":
            self._gui[0]["move_button"].text = "Cancel Move"
            self._gui[0]["delete_button"].is_visible = False
            self._gui[0]["merge_button"].is_visible = False
        elif self._mode == "merge":
            self._gui[0]["merge_button"].text = "Cancel Merge"
            self._gui[0]["move_button"].is_visible = False
            self._gui[0]["delete_button"].is_visible = False

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def draw(self):
        self._game.states["main_game"].draw(True)
        for layer in self._gui[::-1]:
            for component in layer.values():
                component.draw()
