from abc import ABC, abstractmethod


class StateBase(ABC):
    def __init__(self, game, GUIFactory):
        self._game = game
        self._GUIFactory = GUIFactory

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