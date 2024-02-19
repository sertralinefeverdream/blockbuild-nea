from items.GenericItem import GenericItem
import pygame
import math

#uploaded


class ToolItem(GenericItem):
    def __init__(self, game, world, item_id, name, texture, tool_break_sfx_id, quantity=1, max_quantity=1,
                 attack_cooldown=100,
                 use_cooldown=100, attack_range=40, use_range=40, attack_strength=10, default_mine_strength=10,
                 preferred_mine_strength=10, preferred_mine_strength_white_list=None, durability=100):
        super().__init__(game, world, item_id, name, texture, quantity, max_quantity, attack_cooldown, use_cooldown,
                         attack_range, use_range, attack_strength, default_mine_strength, preferred_mine_strength,
                         preferred_mine_strength_white_list)
        self._tool_break_sfx_id = tool_break_sfx_id
        self._durability = durability

    @property
    def durability(self):
        return self._durability

    def attack(self, entity_in_range_of_tool, player_centre_pos):
        if pygame.time.get_ticks() - self._attack_timer >= self._attack_cooldown:
            self._attack_timer = pygame.time.get_ticks()
            self._is_mining = False
            if entity_in_range_of_tool is not None:
                self._durability -= 1
                print(self._durability)
                direction = "right" if entity_in_range_of_tool.centre_position[0] > player_centre_pos[0] else "left"
                entity_in_range_of_tool.health -= self._attack_strength
                entity_in_range_of_tool.aggro()
                entity_in_range_of_tool.knockback(direction, 200)
                if entity_in_range_of_tool.health <= 0 and entity_in_range_of_tool.loot is not None and\
                        not entity_in_range_of_tool.is_killed:
                    remainder = self._world.player.hotbar.pickup_item(
                        self._game.item_factory.create_item(self._game, self._world, entity_in_range_of_tool.loot))
                    if remainder is not None:
                        remainder = self._world.player.inventory.pickup_item(remainder)
                    if remainder is not None:
                        print("INVENTORY FULL!")
            return "attack"

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

        if self._block_currently_mining is not self._block_last_mining or not self._is_mining:
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
            self._durability -= 1
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

    def update(self, player_pos):
        mouse_keys_pressed = pygame.mouse.get_pressed()

        if self._durability <= 0:
            print("SHOULD BREAK")
            self._quantity = 0
            self._game.sfx_handler.play_sfx(self._tool_break_sfx_id, self._game.get_option("game_volume").value)
            return

        if mouse_keys_pressed[0]:
            return self.left_use(player_pos)
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
                "quantity": self._quantity,
                "durability": self._durability
            }
        return data

    def load_state_data(self, data):
        self._quantity = data["quantity"]
        self._durability = data["durability"]
