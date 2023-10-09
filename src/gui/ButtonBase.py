from abc import ABC, abstractmethod
import pygame


class ButtonBase(ABC):
    def __init__(self, surface, pos_x, pos_y, size_x, size_y, click_func, hover_colour=(127, 127, 127), button_colour=(0, 0, 0), outline_thickness=2, outline_colour=(0, 0, 0), is_toggle=False, is_enabled=True, is_visible=True):
        self._surface = surface
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._size_x = size_x
        self._size_y = size_y
        self._click_func = click_func
        self._hover_colour = hover_colour
        self._button_colour = button_colour
        self._current_colour = self._button_colour
        self._outline_colour = outline_colour
        self._outline_thickness = outline_thickness
        self._state = 0
        self._is_toggle = is_toggle
        self._is_enabled = is_enabled
        self._is_visible = is_visible
        self._rect = pygame.Rect((self._pos_x, self._pos_y), (self._size_x, self._size_y))

    @property
    def position(self):
        return (self._pos_x, self._pos_y)

    @position.setter
    def position(self, value):
        print(value)
        if (type(value) is tuple or type(value) is list) and len(value) == 2 and type(value[0]) is float and type(value[1]) is float:
            self._pos_x, self._pos_y = value
        else:
            raise TypeError

    @property
    def size(self):
        return (self._size_x, self._size_y)

    @size.setter
    def size(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2 and type(value[0]) is float and type(value[1]) is float:
            self._size_x, self._size_y = value
        else:
            raise TypeError

    @property
    def state(self):
        return self._state

    @property
    def is_toggle(self):
        return self._is_toggle

    @property
    def is_enabled(self):
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        if type(value) is bool:
            self._is_enabled = value
        else:
            raise TypeError

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        if type(value) is bool:
            self._is_visible = value
        else:
            raise TypeError

    @abstractmethod
    def on_hover_enter(self):
        pass

    @abstractmethod
    def on_hover_leave(self):
        pass

    @abstractmethod
    def on_mouse_click(self):
        pass

    @abstractmethod
    def on_mouse_hold(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass
