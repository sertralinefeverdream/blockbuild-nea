from abc import ABC, abstractmethod


class StateBase(ABC):
    def __init__(self, game, max_framerate):
        self.__game = game
        self.__max_framerate = max_framerate

    @property
    def game(self):
        return self.__game

    @property
    def max_framerate(self):
        return self.__max_framerate

    @abstractmethod
    def on_state_enter(self):
        pass

    @abstractmethod
    def on_state_leave(self):
        pass

    @abstractmethod
    def loop(self):
        pass