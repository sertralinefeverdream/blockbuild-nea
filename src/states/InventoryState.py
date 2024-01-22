from src.states.StateBase import StateBase
import pygame

class InventoryState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._inventory = None
        self._hotbar = None
        self._inventory_key_held = False
        self._item_selected = None # In the form (row_index, column_index, id) where id identifies whether the item originates from the inventory or the hotbar
        self._mode = "default"

    def initialise_gui(self):
        self._gui = [
            {"inventory_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game, self._game.window, 9, 9, self.on_inventory_item_press),
             "hotbar_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game, self._game.window, 1, 9, self.on_hotbar_item_press),
             "move_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window, self.move_button_press)},
            {},
            {}
        ]

    def on_hotbar_item_press(self, item_button):
        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0]["hotbar_display"])
            self._item_selected = (item_button_row, item_button_column, "hotbar")
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0]["hotbar_display"])
            self.swap((item_button_row, item_button_column, "hotbar"), self._item_selected)
            self._mode = "default"

    def on_inventory_item_press(self, item_button):
        if self._mode == "default":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0]["inventory_display"])
            self._item_selected = (item_button_row, item_button_column, "inventory")
        elif self._mode == "move":
            item_button_row, item_button_column = self.find_item_button_indexes_in_display(item_button, self._gui[0]["inventory_display"])
            self.swap((item_button_row, item_button_column, "inventory"), self._item_selected)
            self._mode = "default"

    def swap(self, item_tuple_1, item_tuple_2):
        item_container_1 = self._inventory if item_tuple_1[2] == "inventory" else self._hotbar
        item_container_2 = self._inventory if item_tuple_2[2] == "inventory" else self._hotbar
        temp = item_container_1.get_item_at_index(item_tuple_1[0], item_tuple_1[1])

        item_container_1.set_item_at_index(item_container_2.get_item_at_index(item_tuple_2[0], item_tuple_2[1]), item_tuple_1[0], item_tuple_1[1])
        item_container_2.set_item_at_index(temp, item_tuple_2[0], item_tuple_2[1])

    def find_item_button_indexes_in_display(self, item_button, container_display):
        for row_index, row in enumerate(container_display.gui):
            if item_button in row:
                return row_index, row.index(item_button)
        return None

    def move_button_press(self, button):
        print("TRIGGERED")
        if self._mode == "default":
            if self._item_selected is not None:
                container_to_check = self._inventory if self._item_selected[2] == "inventory" else self._hotbar
                if container_to_check.get_item_at_index(self._item_selected[0], self._item_selected[1]) is not None:
                    self._mode = "move"
        elif self._mode == "move":
            print("CHANGED TO DEFAULT")
            self._mode = "default"

    def on_state_enter(self, params=None):
        self._gui[0]["inventory_display"].centre_position = (600.0, 300.0)
        self._gui[0]["hotbar_display"].centre_position = (600.0, 700.0)

        self._gui[0]["move_button"].centre_position = (250.0, 300.0)
        self._gui[0]["move_button"].size = (100.0, 50.0)

        self._inventory = params[0] if params is not None else None
        self._hotbar = params[1] if params is not None else None
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

        if self._mode == "default":
            self._gui[0]["move_button"].text = "Move Item"
        elif self._mode == "move":
            self._gui[0]["move_button"].text = "Cancel Move"

        print(self._mode)

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def draw(self):
        self._game.states["main_game"].draw(True)
        for layer in self._gui[::-1]:
            for component in layer.values():
                component.draw()


