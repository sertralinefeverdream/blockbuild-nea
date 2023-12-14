from abc import ABC, abstractmethod


class BlockBehaviour(ABC):
    def __init__(self, audio_handler):
        self._block = None
        self._audio_handler = audio_handler

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, value):
        self._block = value

    @abstractmethod
    def update(self):
        pass
