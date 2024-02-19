import pygame
from states.StateBase import StateBase

#uploaded

class ChestInteractState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._inventory = None
        self._hotbar = None
        self._chest = None
        self._item_selected = None
        self._item_display_hovering = None
        self._interact_key_held = False
        self._mode = "default"

    def initialise_gui(self):
        self._gui = [
            {"name_box": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window)},
            {"inventory_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                    self._game.window, 9, 9,
                                                                    self.on_inventory_item_press,
                                                                    self.on_hover_enter,
                                                                    self.on_hover_leave),
             "hotbar_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                 self._game.window, 1, 9,
                                                                 self.on_hotbar_item_press,
                                                                 self.on_hover_enter,
                                                                 self.on_hover_leave),
             "chest_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                self._game.window, 6, 6,
                                                                self.on_chest_item_press,
                                                                self.on_hover_enter,
                                                                self.on_hover_leave),
             "move_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                              self.on_move_button_press),
             "delete_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                self.on_delete_button_press),
             "merge_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                               self.on_merge_button_press)
             },
            {}
        ]

    def on_state_enter(self, params=None):
        self._game.music_handler.set_shuffle_list(["Atmos Sphear", "Aquatic Ambience"])
        if self._game.previous_state is not self._game.states["main_game"]:
            self._game.music_handler.shuffle_play()

        self._gui[1]["inventory_display"].centre_position = (300.0, 300.0)
        self._gui[1]["hotbar_display"].centre_position = (600.0, 700.0)
        self._gui[1]["chest_display"].centre_position = (875.0, 300.0)

        self._gui[1]["move_button"].size = (110.0, 50.0)
        self._gui[1]["move_button"].centre_position = (175.0, 600.0)

        self._gui[1]["delete_button"].size = (110.0, 50.0)
        self._gui[1]["delete_button"].centre_position = (300.0, 600.0)

        self._gui[1]["merge_button"].size = (110.0, 50.0)
        self._gui[1]["merge_button"].centre_position = (425.0, 600.0)

        self._gui[0]["name_box"].font_size = 25
        self._gui[0]["name_box"].text_colour = (255, 255, 255)
        self._gui[0]["name_box"].has_box = False
        self._gui[0]["name_box"].has_outline = False
        self._gui[0]["name_box"].is_visible = False

        self._inventory = params[0] if params is not None else None
        self._hotbar = params[1] if params is not None else None
        self._chest = params[2] if params is not None else None
        self._interact_key_held = False
        self._item_selected = None
        self._item_display_hovering = None
        self._mode = "default"

        self._gui[1]["inventory_display"].container = self._inventory
        self._gui[1]["hotbar_display"].container = self._hotbar
        self._gui[1]["chest_display"].container = self._chest

    def on_state_leave(self, params=None):
        pass

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self._game.keys_pressed[pygame.K_f]:
            self._interact_key_held = True
        elif not self._game.keys_pressed[pygame.K_f] and self._interact_key_held:
            self._game.pop_state()
            self._interact_key_held = False

        self._hotbar.update(None, False)
        self._inventory.update()
        self._chest.update()

        if self._mode == "default":
            self._gui[1]["move_button"].text = "Move Item"
            self._gui[1]["merge_button"].text = "Merge"
            self._gui[1]["delete_button"].text = "Delete"
            if self._item_selected is None:
                self._gui[1]["move_button"].is_visible = False
                self._gui[1]["delete_button"].is_visible = False
                self._gui[1]["merge_button"].is_visible = False
            else:
                self._gui[1]["move_button"].is_visible = True
                self._gui[1]["delete_button"].is_visible = True
                self._gui[1]["merge_button"].is_visible = True

        elif self._mode == "move":
            self._gui[1]["move_button"].text = "Cancel Move"
            self._gui[1]["delete_button"].is_visible = False
            self._gui[1]["merge_button"].is_visible = False
        elif self._mode == "merge":
            self._gui[1]["merge_button"].text = "Cancel Merge"
            self._gui[1]["move_button"].is_visible = False
            self._gui[1]["delete_button"].is_visible = False

        self.update_item_display_currently_hovering()

        if self._item_display_hovering is not None:
            if self._item_display_hovering.item is not None:
                self._gui[0]["name_box"].position = (mouse_pos[0] + 15, mouse_pos[1])
                self._gui[0]["name_box"].text = self._item_display_hovering.item.name
                self._gui[0]["name_box"].is_visible = True
            else:
                self._gui[0]["name_box"].is_visible = False
        else:
            self._gui[0]["name_box"].is_visible = False

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def draw(self):
        self._game.states["main_game"].draw(True)
        for layer in self._gui[::-1]:
            for component in layer.values():
                component.draw()

    def on_hover_enter(self, item_button):
        self._item_display_hovering = item_button

    def on_hover_leave(self, item_button):
        self._item_display_hovering = None

    def on_hotbar_item_press(self, item_button):
        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "hotbar_display"])
            if self._hotbar.get_item_at_index(item_button_row, item_button_column) is not None:
                self._item_selected = (item_button_row, item_button_column, "hotbar")
            else:
                self._item_selected = None
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "hotbar_display"])
            self.swap((item_button_row, item_button_column, "hotbar"), self._item_selected)
            self._item_selected = None
            self._mode = "default"
        elif self._mode == "merge":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "hotbar_display"])
            selected_item_container = self._inventory if self._item_selected[2] == "inventory" else self._hotbar if \
                self._item_selected[2] == "hotbar" else self._chest
            item_1 = selected_item_container.get_item_at_index(self._item_selected[0], self._item_selected[1])
            item_2 = self._hotbar.get_item_at_index(item_button_row, item_button_column)
            if item_2 is not None:
                if item_1.item_id == item_2.item_id and item_1 is not item_2 and item_2.quantity < item_2.max_quantity:
                    self.merge(self._item_selected, (item_button_row, item_button_column, "hotbar"))
                    self._item_selected = None
                    self._mode = "default"

    def on_inventory_item_press(self, item_button):
        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "inventory_display"])
            if self._inventory.get_item_at_index(item_button_row, item_button_column) is not None:
                self._item_selected = (item_button_row, item_button_column, "inventory")
            else:
                self._item_selected = None
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "inventory_display"])
            self.swap((item_button_row, item_button_column, "inventory"), self._item_selected)
            self._item_selected = None
            self._mode = "default"
        elif self._mode == "merge":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "inventory_display"])
            selected_item_container = self._inventory if self._item_selected[2] == "inventory" else self._hotbar if \
                self._item_selected[2] == "hotbar" else self._chest
            item_1 = selected_item_container.get_item_at_index(
                self._item_selected[0], self._item_selected[1])
            item_2 = self._inventory.get_item_at_index(item_button_row, item_button_column)  # MERGING INTO
            if item_2 is not None:
                if item_1.item_id == item_2.item_id and item_1 is not item_2 and item_2.quantity < item_2.max_quantity:
                    self.merge(self._item_selected, (item_button_row, item_button_column, "inventory"))
                    self._item_selected = None
                    self._mode = "default"

    def on_chest_item_press(self, item_button):
        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "chest_display"])
            if self._chest.get_item_at_index(item_button_row, item_button_column) is not None:
                self._item_selected = (item_button_row, item_button_column, "chest")
            else:
                self._item_selected = None
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "chest_display"])
            self.swap((item_button_row, item_button_column, "chest"), self._item_selected)
            self._item_selected = None
            self._mode = "default"
        elif self._mode == "merge":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[1][
                "chest_display"])
            selected_item_container = self._inventory if self._item_selected[2] == "inventory" else self._hotbar if \
                self._item_selected[2] == "hotbar" else self._chest
            item_1 = selected_item_container.get_item_at_index(
                self._item_selected[0], self._item_selected[1])
            item_2 = self._chest.get_item_at_index(item_button_row, item_button_column)  # MERGING INTO
            if item_2 is not None:
                if item_1.item_id == item_2.item_id and item_1 is not item_2 and item_2.quantity < item_2.max_quantity:
                    self.merge(self._item_selected, (item_button_row, item_button_column, "chest"))
                    self._item_selected = None
                    self._mode = "default"

    def find_item_button_indexes_in_display(self, item_button, container_display):
        for row_index, row in enumerate(container_display.gui):
            if item_button in row:
                return row_index, row.index(item_button)
        return None

    def on_move_button_press(self, button):
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_check = self._inventory if self._item_selected[2] == "inventory" else self._hotbar if \
                    self._item_selected[2] == "hotbar" else self._chest
                if container_to_check.get_item_at_index(self._item_selected[0], self._item_selected[1]) is not None:
                    self._mode = "move"
        elif self._mode == "move":
            self._mode = "default"

    def on_delete_button_press(self, button):
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_delete_from = self._inventory if self._item_selected[2] == "inventory" else self._hotbar if \
                    self._item_selected[2] == "hotbar" else self._chest
                if container_to_delete_from.get_item_at_index(self._item_selected[0],
                                                              self._item_selected[1]) is not None:
                    container_to_delete_from.set_item_at_index(self._item_selected[0], self._item_selected[1], None)
                    self._item_selected = None

    def on_merge_button_press(self, button):
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_check = self._inventory if self._item_selected[2] == "inventory" else self._hotbar if \
                    self._item_selected[2] == "hotbar" else self._chest
                if container_to_check.get_item_at_index(self._item_selected[0], self._item_selected[1]) is not None:
                    self._mode = "merge"
        elif self._mode == "merge":
            self._mode = "default"

    def swap(self, item_tuple_1, item_tuple_2):
        item_container_1 = self._inventory if item_tuple_1[2] == "inventory" else self._hotbar if \
            item_tuple_1[2] == "hotbar" else self._chest
        item_container_2 = self._inventory if item_tuple_2[2] == "inventory" else self._hotbar if \
            item_tuple_2[2] == "hotbar" else self._chest
        temp = item_container_1.get_item_at_index(item_tuple_1[0], item_tuple_1[1])

        item_container_1.set_item_at_index(item_tuple_1[0], item_tuple_1[1],
                                           item_container_2.get_item_at_index(item_tuple_2[0], item_tuple_2[1]))
        item_container_2.set_item_at_index(item_tuple_2[0], item_tuple_2[1], temp)

    def merge(self, item_tuple_1, item_tuple_2):
        item_container_1 = self._inventory if item_tuple_1[2] == "inventory" else self._hotbar if \
            item_tuple_1[2] == "hotbar" else self._chest
        item_container_2 = self._inventory if item_tuple_2[2] == "inventory" else self._hotbar if \
            item_tuple_2[2] == "hotbar" else self._chest

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

    def update_item_display_currently_hovering(self):  # Weirdest auto reformat ever??
        self._item_display_hovering = self._gui[1]["hotbar_display"].get_hovering() if \
            self._gui[1]["hotbar_display"].get_hovering() is not None else \
            self._gui[1]["inventory_display"].get_hovering() if \
                self._gui[1]["inventory_display"].get_hovering() is not None else \
                self._gui[1]["chest_display"].get_hovering() if \
                    self._gui[1]["chest_display"].get_hovering() is not None else None
