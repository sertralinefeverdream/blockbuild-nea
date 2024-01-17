from src.entities.EntityBase import EntityBase
from abc import ABC, abstractmethod


class CharacterBase(EntityBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, animation_handler):
        super().__init__(game, world, entity_id, position, size, max_speed)
        self._max_health = max_health
        self._animation_handler = animation_handler

        self._health = self._max_health
        self._is_in_air = False

    @property
    def max_health(self):
        return self._max_health

    @property
    def max_health(self, value):
        if (type(value) is int or type(value) is float) and value >= 1:
            self._max_health = value
            if self._health > self._max_health:
                self._health = self._max_health

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if (type(value) is int or type(value) is float) and value != 0:
            self._health = value
            if self._health > self._max_health:
                self._health = self._max_health

    @property
    def max_velocity(self):
        return self._max_velocity

    @max_velocity.setter
    def max_velocity(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._max_velocity = value

    @property
    def is_in_air(self):
        return self._is_in_air

    @abstractmethod
    def handle_collisions(self, axis):
        pass

