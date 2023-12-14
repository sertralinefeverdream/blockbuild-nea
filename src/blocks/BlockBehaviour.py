from abc import ABC, abstractmethod


class BlockBehaviour(ABC):
    def __init__(self, audio_handler):
        self._block = None
        self._audio_handler = audio_handler

    @property
    def block(self):
        return self._block

    @abstractmethod
    def update(self):
        pass

    def set_block(self, block):
        self._block = block
