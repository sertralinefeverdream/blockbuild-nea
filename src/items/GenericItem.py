import pygame

class GenericItem:
    def __init__(self, game, world, item_id, name, texture, quantity=-1, max_quantity=100, left_use_cooldown=100, right_use_cooldown=100, left_use_range=40, right_use_range=40):
        self._game = game
        self._world = world
        self._item_id = item_id
        self._name = name
        self._texture = texture
        self._quantity = quantity
        self._max_quantity = max_quantity
        self._left_use_cooldown = left_use_cooldown
        self._right_use_cooldown = right_use_cooldown
        self._left_use_range = left_use_range
        self._right_use_range = right_use_range

        print(f'''DUN3PART{self._right_use_range}''')

        self._left_use_timer = pygame.time.get_ticks()
        self._right_use_timer = pygame.time.get_ticks()

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
    def left_use_timer(self):
        return self._left_use_timer

    @left_use_timer.setter
    def left_use_timer(self, value):
        if type(value) is int:
            self._left_use_timer = value

    @property
    def right_use_timer(self):
        return self._right_use_timer

    @right_use_timer.setter
    def right_use_timer(self, value):
        if type(value) is int:
            self._right_use_timer = value

    @property
    def left_use_range(self):
        return self._left_use_range

    @property
    def right_use_range(self):
        return self._right_use_range

    def right_use(self, player_pos):
        pass

    def left_use(self, player_pos):
        pass # Add logic later

    def update(self, player_pos):
        mouse_keys_pressed = pygame.mouse.get_pressed()
        if mouse_keys_pressed[0]:
            if pygame.time.get_ticks() - self._left_use_timer >= self._left_use_cooldown:
                self._left_use_timer = pygame.time.get_ticks()
                self.left_use(player_pos)
        elif mouse_keys_pressed[2]:
            if pygame.time.get_ticks() - self._right_use_timer >= self._right_use_cooldown:
                self._right_use_timer = pygame.time.get_ticks()
                self.right_use(player_pos)

    def get_state_data(self):
        data = \
        {
            "left_use_timer": self._left_use_timer,
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

