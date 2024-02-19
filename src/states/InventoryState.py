from states.StateBase import StateBase
import pygame

#uploaded

class InventoryState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._inventory = None
        self._hotbar = None
        self._inventory_key_held = False
        self._item_selected = None
        self._recipe_selected = None
        self._item_display_hovering = None
        self._mode = "default"
        self._crafting_recipes = {}
        self._world = None

        for item_id, item_data in self._game.config["items"].items():
            if item_data["recipe"] is not None:
                self._crafting_recipes[item_id] = item_data["recipe"]

        # print(self._crafting_recipes)

    def initialise_gui(self):
        self._gui = [
            {"name_box": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window)
             },
            {
                "inventory_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                       self._game.window, 9, 9,
                                                                       self.on_inventory_item_press,
                                                                       self.on_inventory_and_hotbar_hover_enter,
                                                                       self.on_inventory_and_hotbar_hover_leave),
                "hotbar_display": self._game.gui_factory.create_gui("ContainerDisplayInteractive", self._game,
                                                                    self._game.window, 1, 9, self.on_hotbar_item_press,
                                                                    self.on_inventory_and_hotbar_hover_enter,
                                                                    self.on_inventory_and_hotbar_hover_leave),
                "move_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                 self.on_move_button_press),
                "delete_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                   self.on_delete_button_press),
                "merge_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                  self.on_merge_button_press),
                "craft_button": self._game.gui_factory.create_gui("TextButton", self._game, self._game.window,
                                                                  self.on_craft_button_press),
                "item_description_box": self._game.gui_factory.create_gui("TextLabel", self._game, self._game.window),
                "stone_sword_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                              self._game.window,
                                                                              self.on_craft_item_press),
                "iron_sword_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                             self._game.window,
                                                                             self.on_craft_item_press),
                "gold_sword_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                             self._game.window,
                                                                             self.on_craft_item_press),
                "diamond_sword_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                                self._game.window,
                                                                                self.on_craft_item_press),
                "stone_pickaxe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                                self._game.window,
                                                                                self.on_craft_item_press),
                "iron_pickaxe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                               self._game.window,
                                                                               self.on_craft_item_press),
                "gold_pickaxe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                               self._game.window,
                                                                               self.on_craft_item_press),
                "diamond_pickaxe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                                  self._game.window,
                                                                                  self.on_craft_item_press),
                "stone_axe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                            self._game.window,
                                                                            self.on_craft_item_press),
                "iron_axe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                           self._game.window,
                                                                           self.on_craft_item_press),
                "gold_axe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                           self._game.window,
                                                                           self.on_craft_item_press),
                "diamond_axe_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                              self._game.window,
                                                                              self.on_craft_item_press),
                "oak_plank_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                            self._game.window,
                                                                            self.on_craft_item_press),
                "trap_door_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                            self._game.window,
                                                                            self.on_craft_item_press),
                "stick_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                        self._game.window,
                                                                        self.on_craft_item_press),
                "chest_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                        self._game.window,
                                                                        self.on_craft_item_press),
                "respawn_anchor_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                                 self._game.window,
                                                                                 self.on_craft_item_press),
                "stone_brick_craft_button": self._game.gui_factory.create_gui("ImageButton", self._game,
                                                                              self._game.window,
                                                                              self.on_craft_item_press)

            },
            {
                "crafting_background": self._game.gui_factory.create_gui("RectBox", self._game, self._game.window),
            }
        ]

    def on_state_enter(self, params=None):
        print("ENTERING INVENTORY STATE!")
        self._game.music_handler.set_shuffle_list(["Atmos Sphear", "Aquatic Ambience"])
        if self._game.previous_state is not self._game.states["main_game"]:
            self._game.music_handler.shuffle_play()

        self._gui[1]["inventory_display"].centre_position = (300.0, 300.0)
        self._gui[1]["hotbar_display"].centre_position = (600.0, 700.0)

        self._gui[1]["move_button"].size = (110.0, 50.0)
        self._gui[1]["move_button"].centre_position = (175.0, 600.0)

        self._gui[1]["delete_button"].size = (110.0, 50.0)
        self._gui[1]["delete_button"].centre_position = (300.0, 600.0)

        self._gui[1]["merge_button"].size = (110.0, 50.0)
        self._gui[1]["merge_button"].centre_position = (425.0, 600.0)

        self._gui[1]["craft_button"].size = (110.0, 50.0)
        self._gui[1]["craft_button"].centre_position = (630.0, 470.0)
        self._gui[1]["craft_button"].text = "Craft"

        self._gui[1]["item_description_box"].size = (200.0, 50.0)
        self._gui[1]["item_description_box"].font_size = 20
        self._gui[1]["item_description_box"].text = "TEST"
        self._gui[1]["item_description_box"].position = (710.0, 459.0)

        self._gui[0]["name_box"].font_size = 25
        self._gui[0]["name_box"].text_colour = (255, 255, 255)
        self._gui[0]["name_box"].has_box = False
        self._gui[0]["name_box"].has_outline = False
        self._gui[0]["name_box"].is_visible = False

        self._gui[2]["crafting_background"].colour = (125, 50, 0)
        self._gui[2]["crafting_background"].size = (600.0, 400.0)
        self._gui[2]["crafting_background"].box_colour = (200, 200, 200)
        self._gui[2]["crafting_background"].centre_position = (875.0, 230.0)

        self._gui[1]["stone_sword_craft_button"].size = (40.0, 40.0)
        self._gui[1]["stone_sword_craft_button"].image = self._game.item_spritesheet.parse_sprite("stone_sword")
        self._gui[1]["stone_sword_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["stone_sword_craft_button"].centre_position = (710.0, 80.0)
        self._gui[1]["stone_sword_craft_button"].outline_thickness = 3

        self._gui[1]["iron_sword_craft_button"].size = (40.0, 40.0)
        self._gui[1]["iron_sword_craft_button"].image = self._game.item_spritesheet.parse_sprite("iron_sword")
        self._gui[1]["iron_sword_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["iron_sword_craft_button"].centre_position = (710.0, 120.0)
        self._gui[1]["iron_sword_craft_button"].outline_thickness = 3

        self._gui[1]["gold_sword_craft_button"].size = (40.0, 40.0)
        self._gui[1]["gold_sword_craft_button"].image = self._game.item_spritesheet.parse_sprite("gold_sword")
        self._gui[1]["gold_sword_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["gold_sword_craft_button"].centre_position = (710.0, 160.0)
        self._gui[1]["gold_sword_craft_button"].outline_thickness = 3

        self._gui[1]["diamond_sword_craft_button"].size = (40.0, 40.0)
        self._gui[1]["diamond_sword_craft_button"].image = self._game.item_spritesheet.parse_sprite("diamond_sword")
        self._gui[1]["diamond_sword_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["diamond_sword_craft_button"].centre_position = (710.0, 200.0)
        self._gui[1]["diamond_sword_craft_button"].outline_thickness = 3

        self._gui[1]["stone_pickaxe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["stone_pickaxe_craft_button"].image = self._game.item_spritesheet.parse_sprite("stone_pickaxe")
        self._gui[1]["stone_pickaxe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["stone_pickaxe_craft_button"].centre_position = (630.0, 80.0)
        self._gui[1]["stone_pickaxe_craft_button"].outline_thickness = 3

        self._gui[1]["iron_pickaxe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["iron_pickaxe_craft_button"].image = self._game.item_spritesheet.parse_sprite("iron_pickaxe")
        self._gui[1]["iron_pickaxe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["iron_pickaxe_craft_button"].centre_position = (630.0, 120.0)
        self._gui[1]["iron_pickaxe_craft_button"].outline_thickness = 3

        self._gui[1]["gold_pickaxe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["gold_pickaxe_craft_button"].image = self._game.item_spritesheet.parse_sprite("gold_pickaxe")
        self._gui[1]["gold_pickaxe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["gold_pickaxe_craft_button"].centre_position = (630.0, 160.0)
        self._gui[1]["gold_pickaxe_craft_button"].outline_thickness = 3

        self._gui[1]["diamond_pickaxe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["diamond_pickaxe_craft_button"].image = self._game.item_spritesheet.parse_sprite("diamond_pickaxe")
        self._gui[1]["diamond_pickaxe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["diamond_pickaxe_craft_button"].centre_position = (630.0, 200.0)
        self._gui[1]["diamond_pickaxe_craft_button"].outline_thickness = 3

        self._gui[1]["stone_axe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["stone_axe_craft_button"].image = self._game.item_spritesheet.parse_sprite("stone_axe")
        self._gui[1]["stone_axe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["stone_axe_craft_button"].centre_position = (750.0, 80.0)
        self._gui[1]["stone_axe_craft_button"].outline_thickness = 3

        self._gui[1]["iron_axe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["iron_axe_craft_button"].image = self._game.item_spritesheet.parse_sprite("iron_axe")
        self._gui[1]["iron_axe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["iron_axe_craft_button"].centre_position = (750.0, 120.0)
        self._gui[1]["iron_axe_craft_button"].outline_thickness = 3

        self._gui[1]["gold_axe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["gold_axe_craft_button"].image = self._game.item_spritesheet.parse_sprite("gold_axe")
        self._gui[1]["gold_axe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["gold_axe_craft_button"].centre_position = (750.0, 160.0)
        self._gui[1]["gold_axe_craft_button"].outline_thickness = 3

        self._gui[1]["diamond_axe_craft_button"].size = (40.0, 40.0)
        self._gui[1]["diamond_axe_craft_button"].image = self._game.item_spritesheet.parse_sprite("diamond_axe")
        self._gui[1]["diamond_axe_craft_button"].image_scale_multiplier = 0.9
        self._gui[1]["diamond_axe_craft_button"].centre_position = (750.0, 200.0)
        self._gui[1]["diamond_axe_craft_button"].outline_thickness = 3

        self._gui[1]["oak_plank_craft_button"].size = (40.0, 40.0)
        self._gui[1]["oak_plank_craft_button"].image = self._game.block_spritesheet.parse_sprite("oak_plank")
        self._gui[1]["oak_plank_craft_button"].image_scale_multiplier = 0.7
        self._gui[1]["oak_plank_craft_button"].centre_position = (670.0, 80.0)
        self._gui[1]["oak_plank_craft_button"].outline_thickness = 3

        self._gui[1]["stick_craft_button"].size = (40.0, 40.0)
        self._gui[1]["stick_craft_button"].image = self._game.item_spritesheet.parse_sprite("stick")
        self._gui[1]["stick_craft_button"].image_scale_multiplier = 0.7
        self._gui[1]["stick_craft_button"].centre_position = (670.0, 120.0)
        self._gui[1]["stick_craft_button"].outline_thickness = 3

        self._gui[1]["trap_door_craft_button"].size = (40.0, 40.0)
        self._gui[1]["trap_door_craft_button"].image = self._game.block_spritesheet.parse_sprite("trap_door_open")
        self._gui[1]["trap_door_craft_button"].image_scale_multiplier = 0.7
        self._gui[1]["trap_door_craft_button"].centre_position = (670.0, 160.0)
        self._gui[1]["trap_door_craft_button"].outline_thickness = 3

        self._gui[1]["chest_craft_button"].size = (40.0, 40.0)
        self._gui[1]["chest_craft_button"].image = self._game.block_spritesheet.parse_sprite("chest")
        self._gui[1]["chest_craft_button"].image_scale_multiplier = 0.7
        self._gui[1]["chest_craft_button"].centre_position = (670.0, 200.0)
        self._gui[1]["chest_craft_button"].outline_thickness = 3

        self._gui[1]["respawn_anchor_craft_button"].size = (40.0, 40.0)
        self._gui[1]["respawn_anchor_craft_button"].image = self._game.block_spritesheet.parse_sprite("respawn_anchor")
        self._gui[1]["respawn_anchor_craft_button"].image_scale_multiplier = 0.7
        self._gui[1]["respawn_anchor_craft_button"].centre_position = (790.0, 80.0)
        self._gui[1]["respawn_anchor_craft_button"].outline_thickness = 3

        self._gui[1]["stone_brick_craft_button"].size = (40.0, 40.0)
        self._gui[1]["stone_brick_craft_button"].image = self._game.block_spritesheet.parse_sprite("stone_brick")
        self._gui[1]["stone_brick_craft_button"].image_scale_multiplier = 0.7
        self._gui[1]["stone_brick_craft_button"].centre_position = (830.0, 80.0)
        self._gui[1]["stone_brick_craft_button"].outline_thickness = 3

        self._inventory = params[0] if params is not None else None
        self._hotbar = params[1] if params is not None else None
        self._world = params[2] if params is not None else None
        self._inventory_key_held = False
        self._item_selected = None
        self._item_display_hovering = None
        self._mode = "default"

        self._gui[1]["inventory_display"].container = self._inventory
        self._gui[1]["hotbar_display"].container = self._hotbar

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def on_state_leave(self, params=None):
        pass

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self._game.keys_pressed[pygame.K_e]:
            self._inventory_key_held = True
        elif not self._game.keys_pressed[pygame.K_e] and self._inventory_key_held:
            self._game.pop_state()
            self._inventory_key_held = False

        self._hotbar.update(None, False)
        self._inventory.update()

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

            if self._recipe_selected is None:
                self._gui[1]["craft_button"].is_visible = False
                self._gui[1]["item_description_box"].is_visible = False
            else:
                self._gui[1]["craft_button"].is_visible = True
                self._gui[1]["item_description_box"].is_visible = True
                item_name = self._game.config["items"][self._recipe_selected]["name"]
                item_desc = self._crafting_recipes[self._recipe_selected]["description"]
                self._gui[1]["item_description_box"].text = f"{item_name}: {item_desc}"

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

    def update_item_display_currently_hovering(self):  # Weirdest auto reformat ever??
        self._item_display_hovering = self._gui[1]["hotbar_display"].get_hovering() if \
            self._gui[1]["hotbar_display"].get_hovering() is not None else \
            self._gui[1]["inventory_display"].get_hovering() if \
                self._gui[1]["inventory_display"].get_hovering() is not None else None

    def on_craft_button_press(self, button):
        if self.check_can_craft(self._recipe_selected) and self._recipe_selected is not None:
            if self._hotbar.get_remaining_capacity_of_same_type_by_id(
                    self._recipe_selected) + self._inventory.get_remaining_capacity_of_same_type_by_id(
                self._recipe_selected) >= self._game.config["items"][self._recipe_selected]["recipe"]["amount_crafted"]:
                item = self._game.item_factory.create_item(self._game, self._world, self._recipe_selected,
                                                           quantity_override=
                                                           self._crafting_recipes[self._recipe_selected][
                                                               "amount_crafted"])
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
                    pickup_remainder = self._inventory.pickup_item(pickup_remainder)
                if pickup_remainder is not None:
                    print("THIS CASE SHOULDNT BE REACHED EITHER")
            else:
                print(" NOT ENOUGH CAPACITY")
        else:
            print("CANT CRAFT")

    def check_can_craft(self, recipe_id):
        if recipe_id is not None:
            for ingredient_name, quantity_required in self._crafting_recipes[recipe_id]["ingredients"].items():
                if self._hotbar.get_total_quantity_by_id(ingredient_name) + self._inventory.get_total_quantity_by_id(
                        ingredient_name) < quantity_required:
                    print(f"NOT ENOUGH {ingredient_name}")
                    return False
            return True
        else:
            return False

    def on_inventory_and_hotbar_hover_enter(self, item_button):
        self._item_display_hovering = item_button

    def on_inventory_and_hotbar_hover_leave(self, item_button):
        self._item_display_hovering = None

    def on_craft_item_press(self, item_button):
        self._mode = "default"
        self._item_selected = None
        if item_button is self._gui[1]["stone_pickaxe_craft_button"]:
            self._recipe_selected = "stone_pickaxe"
        elif item_button is self._gui[1]["iron_pickaxe_craft_button"]:
            self._recipe_selected = "iron_pickaxe"
        elif item_button is self._gui[1]["oak_plank_craft_button"]:
            self._recipe_selected = "oak_plank_block"
        elif item_button is self._gui[1]["stick_craft_button"]:
            self._recipe_selected = "stick"
        elif item_button is self._gui[1]["gold_pickaxe_craft_button"]:
            self._recipe_selected = "gold_pickaxe"
        elif item_button is self._gui[1]["diamond_pickaxe_craft_button"]:
            self._recipe_selected = "diamond_pickaxe"
        elif item_button is self._gui[1]["stone_sword_craft_button"]:
            self._recipe_selected = "stone_sword"
        elif item_button is self._gui[1]["iron_sword_craft_button"]:
            self._recipe_selected = "iron_sword"
        elif item_button is self._gui[1]["gold_sword_craft_button"]:
            self._recipe_selected = "gold_sword"
        elif item_button is self._gui[1]["diamond_sword_craft_button"]:
            self._recipe_selected = "diamond_sword"
        elif item_button is self._gui[1]["trap_door_craft_button"]:
            self._recipe_selected = "trap_door_block"
        elif item_button is self._gui[1]["chest_craft_button"]:
            self._recipe_selected = "chest_block"
        elif item_button is self._gui[1]["stone_axe_craft_button"]:
            self._recipe_selected = "stone_axe"
        elif item_button is self._gui[1]["iron_axe_craft_button"]:
            self._recipe_selected = "iron_axe"
        elif item_button is self._gui[1]["gold_axe_craft_button"]:
            self._recipe_selected = "gold_axe"
        elif item_button is self._gui[1]["diamond_axe_craft_button"]:
            self._recipe_selected = "diamond_axe"
        elif item_button is self._gui[1]["respawn_anchor_craft_button"]:
            self._recipe_selected = "respawn_anchor_block"
        elif item_button is self._gui[1]["stone_brick_craft_button"]:
            self._recipe_selected = "stone_brick_block"

    def on_hotbar_item_press(self, item_button):
        self._recipe_selected = None
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
