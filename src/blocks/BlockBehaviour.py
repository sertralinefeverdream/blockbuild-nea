from abc import ABC, abstractmethod


class BlockBehaviour(ABC):
    def __init__(self, block):
        self._block = block

    @property
    def block(self):
        return self._block

    @abstractmethod
    def update(self):
        pass
