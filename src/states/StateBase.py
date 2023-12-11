from abc import ABC, abstractmethod


class StateBase(ABC):
    def __init__(self, game, gui_factory, audio_handler_factory):
        self._game = game
        self._gui_factory = gui_factory
        self._audio_handler_factory = audio_handler_factory
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
