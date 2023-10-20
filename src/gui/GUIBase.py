from abc import ABC, abstractmethod


class GUIBase(ABC):
    def __init__(self, surface, position=(0.0, 0.0), size=(50.0, 50.0), is_visible=True):
        self._surface = surface
        self._position = list(position)
        self._size = list(size)
        self._is_visible = is_visible

    @property
    def position(self):
        return self._position

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        if type(value) is bool:
            self._is_visible = value
        else:
            raise TypeError

    @position.setter
    def position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2 and type(value[0]) is float and type(
                value[1]) is float:
            self._position = list(value)
        else:
            raise TypeError

    @property
    def centre_position(self):
        return (self._position[0] + self._size[0] / 2, self._position[1] + self._size[1])

    @centre_position.setter
    def centre_position(self, value):
        if type(value) is tuple or type(value) is list:
            self._position[0] = value[0] - (self._size[0] / 2)
            self._position[1] = value[1] - (self._size[1] / 2)
        else:
            raise TypeError

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2 and type(value[0]) is float and type(
                value[1]) is float:
            self._size = list(value)
        else:
            raise TypeError

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass