from src.entities.EntityBase import EntityBase
from abc import ABC, abstractmethod


class CharacterBase(EntityBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, animation_handler):
        super().__init__(game, world, entity_id, position, size, max_speed)
        self._max_health = max_health
        self._animation_handler = animation_handler

        self._health = self._max_health
        self._footstep_timer = 0
        self._is_in_air = False
        self._is_knockbacked = False

    @property
    def max_health(self):
        return self._max_health

    @max_health.setter
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
        if (type(value) is int or type(value) is float):
            self._health = value
            if self._health > self._max_health:
                self._health = self._max_health
            elif self._health < 0:
                self._health = 0

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

    def knockback(self, direction, strength):
        self._velocity[1] = -240
        self._velocity[0] = strength if direction.lower() == "right" else -strength
        self._is_knockbacked = True

    def jump(self):
        self._velocity[1] = -320

