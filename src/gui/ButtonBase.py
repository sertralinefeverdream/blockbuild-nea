from abc import ABC, abstractmethod
from src.gui.GUIBase import GUIBase
import pygame


class ButtonBase(GUIBase):
    def __init__(self, surface, click_func, position=(0.0, 0.0), size=(50.0, 50.0),  held_func=None, hover_leave_func=None, hover_enter_func=None, hover_colour=(127, 127, 127), button_colour=(0, 0, 0), outline_thickness=2, outline_colour=(0, 0, 0),  is_enabled=True, is_visible=True):
        super().__init__(surface, position, size, is_visible)
        self._click_func = click_func
        self._hover_enter_func = hover_enter_func
        self._hover_leave_func = hover_leave_func
        self._held_func = held_func
        self._hover_colour = hover_colour
        self._button_colour = button_colour
        self._current_colour = self._button_colour
        self._outline_colour = outline_colour
        self._outline_thickness = outline_thickness
        self._is_enabled = is_enabled
        self._is_hovering = False
        self._is_pressed = False
        self._rect = pygame.Rect(self._position, self._size)

    @property
    def is_enabled(self):
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        if type(value) is bool:
            self._is_enabled = value
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

