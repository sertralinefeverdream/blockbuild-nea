from entities.EntityBase import EntityBase
from abc import abstractmethod

#uploaded

class CharacterBase(EntityBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, animation_handler,
                 hurt_sfx_id=None, death_sfx_id=None):
        super().__init__(game, world, entity_id, position, size, max_speed)
        self._max_health = max_health
        self._animation_handler = animation_handler
        self._hurt_sfx_id = hurt_sfx_id
        self._death_sfx_id = death_sfx_id

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
            if value < self._health:
                if self._hurt_sfx_id is not None:
                    self._game.sfx_handler.play_sfx(self._hurt_sfx_id, self._game.get_option("game_volume").value)
                else:
                    print("NON EXISTENT")
            self._health = value
            if self._health > self._max_health:
                self._health = self._max_health
            elif self._health < 0:
                self._health = 0

    @property
    def is_in_air(self):
        return self._is_in_air

    @abstractmethod
    def handle_collisions(self, axis):
        pass

    def kill(self, play_sfx=True):
        if self._death_sfx_id is not None and play_sfx:
            self._game.sfx_handler.play_sfx(self._death_sfx_id, self._game.get_option("game_volume").value)
        self._is_killed = True

    def knockback(self, direction, strength):
        if not self._is_knockbacked:
            self._velocity[1] = -240
        self._velocity[0] = strength if direction.lower() == "right" else -strength
        self._is_knockbacked = True

    def jump(self):
        self._velocity[1] = -320
