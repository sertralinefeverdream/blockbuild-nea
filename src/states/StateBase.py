from abc import ABC, abstractmethod

#upladed

class StateBase(ABC):
    def __init__(self, game):
        self._game = game
        self._gui = {}
        self.initialise_gui()

    @property
    def game(self):
        return self._game

    @abstractmethod
    def initialise_gui(self):
        pass

    @abstractmethod
    def on_state_enter(self, params=None):
        pass

    @abstractmethod
    def on_state_leave(self, params=None):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
