import pygame
from abc import ABC, abstractmethod
import json


class BlockBase(ABC):
    def __init__(self, game, block_id, sfx_handler, texture, break_sfx_id, place_sfx_id, footstep_sfx_id):
        self._game = game
        self._block_id = block_id
        self._sfx_handler = sfx_handler
        self._texture = pygame.transform.scale(texture, (40, 40))
        self._break_sfx_id = break_sfx_id
        self._place_sfx_id = place_sfx_id
        self._footstep_sfx_id = footstep_sfx_id

        self.init_audio()

    @property
    def game(self):
        return self._game

    @property
    def block_id(self):
        return self._block_id

    @property
    def sfx_handler(self):
        return self._sfx_handler

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = pygame.transform.scale(self._texture, (40, 40))

    @property
    def break_sfx_id(self):
        return self._break_sfx_id

    @break_sfx_id.setter
    def break_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._break_sfx_id = value
            self._sfx_handler.add_sfx(value, self._game.config["sfx_assets"][value])

    @property
    def place_sfx_id(self):
        return self._place_sfx_id

    @place_sfx_id.setter
    def place_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._place_sfx_id = value
            self._sfx_handler.add_sfx(value, self._game.config["sfx_assets"][value])

    @property
    def footstep_sfx_id(self):
        return self._footstep_sfx_id

    @footstep_sfx_id.setter
    def footstep_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._footstep_sfx_id = value
            self._sfx_handler.add_sfx(value, self._game.config["sfx_assets"][value])

    @abstractmethod
    def init_audio(self):
        pass

    ''' IMPLEMENT SIMILAR IN SUBCLASS IMPLEMENTATION OF INIT_AUDIO ^^^^^
    self._sfxhandler.add_sfx_from_dict(
            {
                self._click_sfx_id: self._game.config["sfx_assets"][self._click_sfx_id],
                self._hover_enter_sfx_id: self._game.config["sfx_assets"][self._hover_enter_sfx_id],
                self._hover_leave_sfx_id: self._game.config["sfx_assets"][self._hover_enter_sfx_id],
                self._disabled_click_sfx_id: self._game.config["sfx_assets"][self._hover_enter_sfx_id]
            }
        )
    '''

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen_position):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def get_state_data(self):
        pass

    # To be implemented differently in subclasses !! State data includes things that are not constant thru out runtime e.g.
    # a loottable of what will be dropped i guess lol

    def serialize(self):
        data = \
            {
                "block_id": f"{self._block_id}",
                "state_data": self.get_state_data()
            }
        return json.dumps(data)