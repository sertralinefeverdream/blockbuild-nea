import pygame
from abc import ABC, abstractmethod

# Cleaned up
#uploaded
class BlockBase(ABC):
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, loot_drop_id=None, loot_drop_tool_whitelist=None, can_collide=True):
        self._game = game
        self._world = world
        self._position = list(position)
        self._hardness = hardness
        self._block_id = block_id
        self._texture = pygame.transform.scale(texture.convert_alpha(), (40, 40))
        self._mine_sfx_id = mine_sfx_id
        self._place_and_break_sfx_id = place_and_break_sfx_id
        self._footstep_sfx_id = footstep_sfx_id
        self._loot_drop_id = loot_drop_id
        self._loot_drop_tool_whitelist = loot_drop_tool_whitelist
        self._can_collide = can_collide

        self._hitbox = pygame.Rect(self._world.camera.get_screen_position(self._position), (40, 40))
        self._is_broken = False

    @property
    def game(self):
        return self._game

    @property
    def world(self):
        return self._world

    @property
    def position(self):
        return self._position

    @property
    def hardness(self):
        return self._hardness

    @property
    def block_id(self):
        return self._block_id

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = pygame.transform.scale(value.convert_alpha(), (40, 40))
            self.enable_flag_for_region_redraw()

    @property
    def mine_sfx_id(self):
        return self._mine_sfx_id

    @mine_sfx_id.setter
    def mine_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._mine_sfx_id = value

    @property
    def place_and_break_sfx_id(self):
        return self._place_and_break_sfx_id

    @place_and_break_sfx_id.setter
    def place_and_break_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._place_and_break_sfx_id = value

    @property
    def footstep_sfx_id(self):
        return self._footstep_sfx_id

    @footstep_sfx_id.setter
    def footstep_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._footstep_sfx_id = value

    @property
    def loot_drop_id(self):
        return self._loot_drop_id

    @property
    def loot_drop_tool_whitelist(self):
        return self._loot_drop_tool_whitelist

    @property
    def can_collide(self):
        return self._can_collide

    @can_collide.setter
    def can_collide(self, value):
        if type(value) is bool:
            self._can_collide = value

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def is_broken(self):
        return self._is_broken

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_state_data(self):
        pass

    @abstractmethod
    def load_state_data(self, data):
        pass


    def enable_flag_for_region_redraw(self):  # Call when visual change requires the region to be redrawn.
        region = self._world.get_region_at_position(self._position)
        region.enable_flag_for_redraw()

    # Block save data function
    def convert_data(self):  # Overrideable in subclasses. Must follow similar form.
        data = \
            {
                "block_id": self._block_id,
                "state_data": self.get_state_data()
            }
        return data

    def kill(self):
        self._game.sfx_handler.play_sfx(self._place_and_break_sfx_id, self._game.get_option("game_volume").value)
        self._is_broken = True
