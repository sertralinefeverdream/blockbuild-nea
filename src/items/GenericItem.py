import pygame
import math

#uploaded

class GenericItem:  # Can be used for normal items, default_items, etc lol
    def __init__(self, game, world, item_id, name, texture, quantity=1, max_quantity=100, attack_cooldown=100,
                 use_cooldown=100, attack_range=40, use_range=40, attack_strength=10, default_mine_strength=10,
                 preferred_mine_strength=10, preferred_mine_strength_white_list=None):
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
    def item_id(self):
        return self._item_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(value) is str:
            self._name = value

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

    def update(self, player_centre_pos):
        mouse_keys_pressed = pygame.mouse.get_pressed()

        if mouse_keys_pressed[0]:
            return self.left_use(player_centre_pos)
        elif not mouse_keys_pressed[0]:
            self._is_mining = False
            self._mine_sound_timer = 0
            if self._block_currently_mining is not None:
                self._block_currently_mining_hardness_remaining = self._block_currently_mining.hardness

        if mouse_keys_pressed[2]:
            if pygame.time.get_ticks() - self._use_timer >= self._use_cooldown:
                self._use_timer = pygame.time.get_ticks()
                self.right_use(player_centre_pos)

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

    def left_use(self, player_centre_pos):
        mouse_pos = pygame.mouse.get_pos()
        mouse_world_pos = self._world.camera.get_world_position(mouse_pos)
        delta_time = self._game.clock.get_time() / 1000

        entity_in_range_of_tool = self.get_entity_in_range_of_tool(player_centre_pos, mouse_pos, self._attack_range)

        if entity_in_range_of_tool is not None:  # If an entity is within range attack and forgo mining completely
            self._is_mining = False
            return self.attack(entity_in_range_of_tool, player_centre_pos)

        self._block_last_mining = self._block_currently_mining
        self._block_currently_mining = self._world.get_block_at_position(mouse_world_pos)

        if self._block_currently_mining is None:  # If trying to mine air block
            self._is_mining = False
            return self.attack(entity_in_range_of_tool, player_centre_pos)
        elif self._block_currently_mining is not None and math.sqrt(  # If out of range entirely
                (self._block_currently_mining.position[0] - player_centre_pos[0]) ** 2 + (
                        self._block_currently_mining.position[1] - player_centre_pos[1]) ** 2) > self._use_range:
            self._is_mining = False
            return self.attack(entity_in_range_of_tool, player_centre_pos)

        if self._block_currently_mining is not self._block_last_mining or self._is_mining == False:
            self._block_currently_mining_hardness_remaining = self._block_currently_mining.hardness

        self._is_mining = True

        if self._block_currently_mining.block_id in self._preferred_mine_strength_whitelist:
            self._block_currently_mining_hardness_remaining -= (self._preferred_mine_strength) * delta_time
        else:
            self._block_currently_mining_hardness_remaining -= (self._default_mine_strength) * delta_time

        if pygame.time.get_ticks() - self._mine_sound_timer >= 250:
            self._game.sfx_handler.play_sfx(self._block_currently_mining.mine_sfx_id,
                                            self._game.get_option("game_volume").value)
            self._mine_sound_timer = pygame.time.get_ticks()

        if self._block_currently_mining_hardness_remaining <= 0:
            can_be_picked_up = True
            if self._block_currently_mining.loot_drop_id is not None:
                if self._block_currently_mining.loot_drop_tool_whitelist is not None:
                    if self._item_id not in self._block_currently_mining.loot_drop_tool_whitelist:
                        can_be_picked_up = False
                if can_be_picked_up:
                    remainder = self._world.player.hotbar.pickup_item(
                        self._game.item_factory.create_item(self._game, self._world,
                                                            self._block_currently_mining.loot_drop_id))
                    if remainder is not None:
                        print("FILL UP INVENTORY")
                        remainder = self._world.player.inventory.pickup_item(remainder)
                    if remainder is not None:
                        print("INVENTORY FULL!")
                else:
                    print("CANT BE PICKED UP!")
            else:
                print("LOOT DROP ID IS NONE")
            self._block_currently_mining.kill()

    def right_use(self, player_centre_pos):
        pass

    def get_entity_in_range_of_tool(self, player_centre_pos, mouse_pos, range):
        world_mouse_pos = self._world.camera.get_world_position(mouse_pos)
        distance_x = abs(world_mouse_pos[0] - player_centre_pos[0])
        distance_y = abs(world_mouse_pos[1] - player_centre_pos[1])
        distance_away = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if distance_away == 0:
            return None
        theta = math.acos(distance_x / distance_away)
        dx = 10 * math.cos(theta)
        dy = 10 * math.sin(theta)

        if world_mouse_pos[0] < player_centre_pos[0]:
            dx *= -1
        if world_mouse_pos[1] < player_centre_pos[1]:
            dy *= -1

        current_point = [player_centre_pos[0], player_centre_pos[1]]
        index = 0
        while index <= range:
            block_at_point = self._world.get_block_at_position(current_point)
            if block_at_point is None or (block_at_point is not None and not block_at_point.can_collide):
                entities_at_point = self._world.get_entities_at_position(current_point)
                if len(entities_at_point) > 0:
                    if len(entities_at_point) > 1:
                        entities_at_point.sort(key=lambda x: math.sqrt(
                            ((x.centre_position[0]) - (player_centre_pos[0])) ** 2 + (
                                    (x.centre_position[1]) - (player_centre_pos[1])) ** 2))
                    return entities_at_point[0]
            else:
                return None

            current_point[0] += dx
            current_point[1] += dy
            index += 10
        return None

    def attack(self, entity_in_range_of_tool, player_centre_pos):
        if pygame.time.get_ticks() - self._attack_timer >= self._attack_cooldown:
            self._attack_timer = pygame.time.get_ticks()
            self._is_mining = False
            if entity_in_range_of_tool is not None:
                direction = "right" if entity_in_range_of_tool.centre_position[0] > player_centre_pos[0] else "left"
                entity_in_range_of_tool.health -= self._attack_strength
                entity_in_range_of_tool.aggro()
                entity_in_range_of_tool.knockback(direction, 200)
                if entity_in_range_of_tool.health <= 0 and entity_in_range_of_tool.loot is not None and\
                        not entity_in_range_of_tool.is_killed:
                    remainder = self._world.player.hotbar.pickup_item(
                        self._game.item_factory.create_item(self._game, self._world,
                                                            entity_in_range_of_tool.loot))
                    if remainder is not None:
                        remainder = self._world.player.inventory.pickup_item(remainder)
                    if remainder is not None:
                        print("INVENTORY FULL!")
            return "attack"

    def get_state_data(self):
        data = \
            {
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
        self._quantity = data["quantity"]
