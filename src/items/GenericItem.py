import pygame

class GenericItem:
    def __init__(self, game, world, name, texture, quantity=1, max_quantity=100, can_be_stacked=True, left_use_cooldown=100, right_use_cooldown=100):
        self._game = game
        self._world = world
        self._name = name
        self._texture = texture
        self._quantity = quantity
        self._max_quantity = max_quantity
        self._can_be_stacked = can_be_stacked
        self._left_use_cooldown = left_use_cooldown
        self._right_use_cooldown = right_use_cooldown

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
    def can_be_stacked(self):
        return self._can_be_stacked

    def right_use(self):
        pass

    def left_use(self):
        pass

    def update(self):
        mouse_keys_pressed = pygame.mouse.get_pressed()
        if mouse_keys_pressed[0]:
            if pygame.time.get_ticks() - self._left_use_timer >= self._left_use_cooldown:
                self._left_use_timer = pygame.time.get_ticks()
                self.left_use()
        elif mouse_keys_pressed[2]:
            if pygame.time.get_ticks() - self._right_use_timer >= self._right_use_cooldown:
                self._right_use_timer = pygame.time.get_ticks()
                self.right_use()

