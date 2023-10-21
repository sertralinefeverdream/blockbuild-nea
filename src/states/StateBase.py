from abc import ABC, abstractmethod


class StateBase(ABC):
    def __init__(self, game, music_assets={}, sfx_assets={}):
        self._game = game
        self._music_assets = music_assets
        self._sfx_assets = sfx_assets

    @property
    def game(self):
        return self._game

    @abstractmethod
    def on_state_enter(self):
        pass

    @abstractmethod
    def on_state_leave(self):
        pass

    @abstractmethod
    def loop(self):
        pass