import pygame
from abc import ABC, abstractmethod
import json


class BlockBase(ABC):
    def __init__(self, game, world, position, block_id, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        self._game = game
        self._world = world
        self._position = list(position)
        self._block_id = block_id
        self._texture = pygame.transform.scale(texture, (40, 40))
        self._break_sfx_id = break_sfx_id
        self._place_sfx_id = place_sfx_id
        self._footstep_sfx_id = footstep_sfx_id

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
    def block_id(self):
        return self._block_id

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = pygame.transform.scale(self._texture, (40, 40))
            self.enable_flag_for_region_redraw()

    @property
    def break_sfx_id(self):
        return self._break_sfx_id

    @break_sfx_id.setter
    def break_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._break_sfx_id = value

    @property
    def place_sfx_id(self):
        return self._place_sfx_id

    @place_sfx_id.setter
    def place_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._place_sfx_id = value

    @property
    def footstep_sfx_id(self):
        return self._footstep_sfx_id

    @footstep_sfx_id.setter
    def footstep_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._footstep_sfx_id = value

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
        return None

    # To be implemented differently in subclasses !! State data includes things that are not constant thru out runtime e.g.
    # a loottable of what will be dropped i guess in the case of some future container block akin to a chest or storage block.

    def enable_flag_for_region_redraw(self): # Call when visual change requires the region to be redrawn.
        region = self._world.get_region_at_position(self._position)
        region.enable_flag_for_redraw()

    def serialize(self):
        return json.dumps(self.convert_data())

    def convert_data(self): #Overrideable in subclasses. Must follow similar form.
        data = \
            {
                "block_id": f"{self._block_id}",
                "state_data": self.get_state_data()
            }
        return data

    def kill(self):
        self._game.sfx_handler.play_sfx(self._break_sfx_id, 1)
        self._is_broken = True
