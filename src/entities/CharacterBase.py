from src.entities.EntityBase import EntityBase
from abc import ABC, abstractmethod


class CharacterBase(EntityBase):
    def __init__(self, game, world, entity_id, position, size, texture, max_health):
        super().__init__(game, world, entity_id, position, size, texture)
        self._max_health = max_health

        self._health = self._max_health

    @property
    def max_health(self):
        return self._max_health

    @property
    def max_health(self, value):
        if (type(value) is int or type(value) is float) and value >= 1:
            self._max_health = value

    @abstractmethod
    def handle_collisions(self, axis):
        pass

    def damage(self, value):
        if (type(value) is int or type(value) is float) and value > 0:
            self._health -= value
            if self._health <= 0:
                self._health = 0
                self.kill()
