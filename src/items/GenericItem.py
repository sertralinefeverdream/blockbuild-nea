import pygame

class GenericItem: # Can be used for normal items, tools, default, etc
    def __init__(self, game, world, item_id, name, texture, quantity=-1, max_quantity=100, attack_cooldown=100, use_cooldown=100, attack_range=40, use_range=40, attack_strength=10, default_mining_strength=10, preferred_mining_strength=10, preferred_mining_strength_white_list=None):
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
        self._default_mining_strength = default_mining_strength
        self._preferred_mining_strength = preferred_mining_strength

        if preferred_mining_strength_white_list is None:
            self._preferred_mining_strength_whitelist = []
        else:
            self._preferred_mining_strength_whitelist = preferred_mining_strength_white_list

        print(f'''DUN3PART{self._use_range}''')

        self._attack_timer = 0
        self._right_use_timer = 0
        self._mine_sound_timer = 0
        self._block_last_hovering = None
        self._block_currently_hovering = None
        self._block_currently_hovering_hardness_remaining = 100
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
    def right_use_timer(self):
        return self._right_use_timer

    @right_use_timer.setter
    def right_use_timer(self, value):
        if type(value) is int:
            self._right_use_timer = value

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
    def block_currently_hovering(self):
        return self._block_currently_hovering

    @property
    def block_currently_hovering_hardness_remaining(self):
        return self._block_currently_hovering_hardness_remaining

    def right_use(self, player_pos):
        pass

    def left_use(self, player_pos):
        mouse_pos = pygame.mouse.get_pos()
        world_pos_from_mouse = self._world.camera.get_world_position(mouse_pos)
        delta_time = self._game.clock.get_time() / 1000

        if self._block_currently_hovering is None:
            self._block_currently_hovering_hardness_remaining = 0
            self._is_mining = False
            return
        else:
            self._is_mining = True

        if self._block_currently_hovering is not self._block_last_hovering:
            self._block_currently_hovering_hardness_remaining = self._block_currently_hovering.hardness

        if self._block_currently_hovering.block_id in self._preferred_mining_strength_whitelist:
            print("USING PREFERED")
            self._block_currently_hovering_hardness_remaining -= (self._preferred_mining_strength) * delta_time
        else:
            self._block_currently_hovering_hardness_remaining -= (self._default_mining_strength) * delta_time

        if pygame.time.get_ticks() - self._mine_sound_timer >= 250:
            self._game.sfx_handler.play_sfx(self._block_currently_hovering.break_sfx_id, self._game.get_option("game_volume").value)
            self._mine_sound_timer = pygame.time.get_ticks()

        if self._block_currently_hovering_hardness_remaining <= 0:
                self._block_currently_hovering.kill()

    def update(self, player_pos):
        mouse_keys_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        world_pos_from_mouse = self._world.camera.get_world_position(mouse_pos)

        self._block_last_hovering = self._block_currently_hovering
        self._block_currently_hovering = self._world.get_block_at_position(world_pos_from_mouse)

        if mouse_keys_pressed[0]:
            self.left_use(player_pos)
        else:
            self._block_currently_hovering_hardness_remaining = self._block_currently_hovering.hardness if self._block_currently_hovering is not None else 0
            self._mine_sound_timer = 0
            self._is_mining = False

        if mouse_keys_pressed[2]:
            if pygame.time.get_ticks() - self._right_use_timer >= self._use_cooldown:
                print("CALLED FROM UPDATE RIGHT USE")
                self._right_use_timer = pygame.time.get_ticks()
                self.right_use(player_pos)

    def get_state_data(self):
        data = \
        {
            "attack_timer": self._attack_timer,
            "right_use_timer": self._right_use_timer,
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

    def serialize(self):
        pass

