from abc import ABC, abstractmethod


class StateBase(ABC):
    def __init__(self, game, GUIFactory, AudioHandlerFactory):
        self._game = game
        self._GUIFactory = GUIFactory
        self._AudioHandlerFactory = AudioHandlerFactory
        self._gui = {}
        self.initialise_gui()

    @property
    def game(self):
        return self._game

    @abstractmethod
    def initialise_gui(self):
        pass

    @abstractmethod
    def on_state_enter(self):
        pass

    @abstractmethod
    def on_state_leave(self):
        pass

    @abstractmethod
    def update(self):
        pass
