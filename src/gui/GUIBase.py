from abc import ABC, abstractmethod

#uploaded

class GUIBase(ABC):
    def __init__(self, game, surface, position=(0.0, 0.0), is_visible=True):
        self._game = game
        self._surface = surface
        self._position = list(position)
        self._is_visible = is_visible

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._position = list(value)

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        if type(value) is bool:
            self._is_visible = value

    @property
    @abstractmethod
    def centre_position(self):
        pass

    @centre_position.setter
    @abstractmethod
    def centre_position(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
