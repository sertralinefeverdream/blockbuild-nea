import pygame
from abc import ABC, abstractmethod

#uploaded

class EntityBase:
    def __init__(self, game, world, entity_id, position, size, max_speed):
        self._game = game
        self._world = world
        self._entity_id = entity_id
        self._position = list(position)
        self._size = list(size)
        self._texture = None
        self._max_speed = list(max_speed)

        self._velocity = [0, 0]
        self._hitbox = pygame.Rect((0, 0), self._size)
        self._is_killed = False

    @property
    def game(self):
        return self._game

    @property
    def world(self):
        return self._world

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):
        if type(value) is str:
            self._entity_id = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._position = list(value)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._size = value
            self.update_texture_and_sizes()

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = value
            self.update_texture_and_sizes()

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._velocity = value

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def is_killed(self):
        return self._is_killed

    @is_killed.setter
    def is_killed(self, value):
        if type(value) is bool:
            self._is_killed = value

    @property
    def centre_position(self):
        return self._position[0] + self._size[0] / 2, self._position[1] + self._size[1] / 2

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._position[0] = value[0] - self._size[0] / 2
            self._position[1] = value[1] - self._size[1] / 2

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def get_state_data(self):
        pass

    @abstractmethod
    def load_state_data(self, data):
        pass

    # Entity save data
    def convert_data(self):
        data = {
            "entity_id": self._entity_id,
            "state_data": self.get_state_data()
        }
        return data

    def update_texture_and_sizes(self):  # Call when texture or size changes
        self._texture = pygame.transform.scale(self._texture, self._size)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)

    def kill(self):  # Can be overriden
        self._is_killed = True
