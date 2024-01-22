import pygame
import math

class GenericItem: # Can be used for normal items, tools, default, etc lol
    def __init__(self, game, world, item_id, name, texture, quantity=1, max_quantity=100, attack_cooldown=100, use_cooldown=100, attack_range=40, use_range=40, attack_strength=10, default_mine_strength=10, preferred_mine_strength=10, preferred_mine_strength_white_list=None):
        self._game = game
        self._world = world
        self._item_id = item_id
        self._name = name
        self._texture = texture
        self._quantity = quantity
        self._max_quantity = max_quantity
        self._attack_cooldown = attack_cooldown
        self._use_cooldown = use_cooldown
        self._attack_range = attack_range
        self._use_range = use_range
        self._attack_strength = attack_strength
        self._default_mine_strength = default_mine_strength
        self._preferred_mine_strength = preferred_mine_strength

        if preferred_mine_strength_white_list is None:
            self._preferred_mine_strength_whitelist = []
        else:
            self._preferred_mine_strength_whitelist = preferred_mine_strength_white_list

        self._attack_timer = 0
        self._use_timer = 0
        self._mine_sound_timer = 0
        self._block_last_mining = None
        self._block_currently_mining = None
        self._block_currently_mining_hardness_remaining = 0
        self._is_mining = False

    @property
    def game(self):
        return self._game

    @property
    def world(self):
        return self._world

    @property
    def name(self):
        return self._name

    @property
    def item_id(self):
        return self._item_id

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = value.convert()

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if type(value) is int and value <= self._max_quantity:
            self._quantity = value

    @property
    def max_quantity(self):
        return self._max_quantity

    @max_quantity.setter
    def max_quantity(self, value):
        if type(value) is int:
            self._max_quantity = value
            if self._max_quantity < self._quantity:
                self._quantity = self._max_quantity

    @property
    def attack_timer(self):
        return self._attack_timer

    @attack_timer.setter
    def attack_timer(self, value):
        if type(value) is int:
            self._attack_timer = value

    @property
    def use_timer(self):
        return self._use_timer

    @use_timer.setter
    def use_timer(self, value):
        if type(value) is int:
            self._use_timer = value

    @property
    def attack_range(self):
        return self._attack_range

    @property
    def use_range(self):
        return self._use_range

    @property
    def is_mining(self):
        return self._is_mining

    @property
    def block_currently_mining(self):
        return self._block_currently_mining

    @property
    def block_currently_mining_hardness_remaining(self):
        return self._block_currently_mining_hardness_remaining

    def right_use(self, player_pos):
        pass

    def on_equip(self):
        self._attack_timer = 0
        self._use_timer = 0
        self._mine_sound_timer = 0
        self._block_last_mining = None
        self._block_currently_mining = None
        self._block_currently_mining_hardness_remaining = 0
        self._is_mining = False

    def on_unequip(self):
        pass

    def left_use(self, player_pos):
        mouse_pos = pygame.mouse.get_pos()
        mouse_world_pos = self._world.camera.get_world_position(mouse_pos)
        delta_time = self._game.clock.get_time() / 1000

        self._block_last_mining = self._block_currently_mining
        self._block_currently_mining = self._world.get_block_at_position(mouse_world_pos)

        if self._block_currently_mining is None:
            self._is_mining = False
            return
        elif self._block_currently_mining is not None and math.sqrt((self._block_currently_mining.position[0] - player_pos[0])**2 + (self._block_currently_mining.position[1] - player_pos[1])**2) > self._use_range:
            self._is_mining = False
            return
        else:
            self._is_mining = True

        if self._block_currently_mining is not self._block_last_mining:
            self._block_currently_mining_hardness_remaining = self._block_currently_mining.hardness

        if self._block_currently_mining.block_id in self._preferred_mine_strength_whitelist:
            self._block_currently_mining_hardness_remaining -= (self._preferred_mine_strength) * delta_time
        else:
            self._block_currently_mining_hardness_remaining -= (self._default_mine_strength) * delta_time

        if pygame.time.get_ticks() - self._mine_sound_timer >= 250:
            self._game.sfx_handler.play_sfx(self._block_currently_mining.mine_sfx_id, self._game.get_option("game_volume").value)
            self._mine_sound_timer = pygame.time.get_ticks()

        '''
                if self._block_currently_mining_hardness_remaining <= 0:
                if self._block_currently_mining.loot_drop_id is not None:
                    if self._block_currently_mining.loot_drop_tool_whitelist is not None:
                        if self._item_id in self._block_currently_mining.loot_drop_tool_whitelist:
                            remainder = self._world.player.hotbar.pickup_item(
                                self._game.item_factory.create_item(self._game, self._world, self._block_currently_mining.loot_drop_id))
                            if remainder is not None:
                                print("FILL UP INVENTORY")
                                remainder = self._world.player.inventory.pickup_item(remainder)
                            if remainder is not None:
                                print("INVENTORY FULL!")
                    else:
                        remainder = self._world.player.hotbar.pickup_item(
                            self._game.item_factory.create_item(self._game, self._world,
                                                                self._block_currently_mining.loot_drop_id))
                        if remainder is not None:
                            print("FILL UP INVENTORY")
                            remainder = self._world.player.inventory.pickup_item(remainder)
                        if remainder is not None:
                            print("INVENTORY FULL!")
                else:
                    print("LOOT DROP ID IS NONE")

                self._block_currently_mining.kill()
        '''

        if self._block_currently_mining_hardness_remaining <= 0:
            if self._block_currently_mining.loot_drop_id is not None:
                if self._block_currently_mining.loot_drop_tool_whitelist is not None:
                    if self._item_id not in self._block_currently_mining.loot_drop_tool_whitelist:
                        return None
                remainder = self._world.player.hotbar.pickup_item(
                    self._game.item_factory.create_item(self._game, self._world, self._block_currently_mining.loot_drop_id))
                if remainder is not None:
                    print("FILL UP INVENTORY")
                    remainder = self._world.player.inventory.pickup_item(remainder)
                if remainder is not None:
                    print("INVENTORY FULL!")
            else:
                print("LOOT DROP ID IS NONE")

            self._block_currently_mining.kill()


    def update(self, player_pos):
        mouse_keys_pressed = pygame.mouse.get_pressed()

        if mouse_keys_pressed[0]:
            self.left_use(player_pos)
        elif not mouse_keys_pressed[0]:
            self._is_mining = False
            self._mine_sound_timer = 0
            if self._block_currently_mining is not None:
                self._block_currently_mining_hardness_remaining = self._block_currently_mining.hardness

        if mouse_keys_pressed[2]:
            if pygame.time.get_ticks() - self._use_timer >= self._use_cooldown:
                self._use_timer = pygame.time.get_ticks()
                self.right_use(player_pos)

    def get_state_data(self):
        data = \
        {
            "attack_timer": self._attack_timer,
            "use_timer": self._use_timer,
            "quantity": self._quantity
        }
        return data

    def convert_data(self):
        data = \
        {
            "item_id": self._item_id,
            "state_data": self.get_state_data()
        }
        return data

    def load_state_data(self, data):
        self._attack_timer = data["attack_timer"]
        self._use_timer = data["use_timer"]
        self._quantity = data["quantity"]

