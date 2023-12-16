import pygame
from abc import ABC, abstractmethod


class BlockBase(ABC):
    def __init__(self, game, sfx_handler, texture, break_sound_id, place_sound_id, footstep_sound_id=None):
        self._game = game
        self._sfx_handler = sfx_handler
        self._texture = pygame.transform.scale(texture, (40, 40))

        self.init_audio()

    @property
    def game(self):
        return self._game

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = pygame.transform.scale(self._texture, (40, 40))

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
    def draw(self):
        pass
