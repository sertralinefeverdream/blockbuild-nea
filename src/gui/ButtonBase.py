from abc import abstractmethod
from gui.GUIBase import GUIBase
import pygame

#uploaded

class ButtonBase(GUIBase):
    def __init__(self, game, surface, click_func, click_sfx_id=None, hover_enter_sfx_id=None,
                 hover_leave_sfx_id=None, disabled_click_sfx_id=None, position=(0.0, 0.0), size=(100, 100),
                 held_func=None, hover_leave_func=None, hover_enter_func=None, hover_colour=(127, 0, 0),
                 button_colour=(255, 0, 0), outline_thickness=5, outline_colour=(0, 0, 0), has_box=True,
                 has_outline=True, is_enabled=True,
                 is_visible=True):
        super().__init__(game, surface, position, is_visible)
        self._click_func = click_func
        self._click_sfx_id = click_sfx_id
        self._hover_enter_sfx_id = hover_enter_sfx_id
        self._hover_leave_sfx_id = hover_leave_sfx_id
        self._disabled_click_sfx_id = disabled_click_sfx_id
        self._size = list(size)
        self._held_func = held_func
        self._hover_leave_func = hover_leave_func
        self._hover_enter_func = hover_enter_func
        self._hover_colour = list(hover_colour)
        self._button_colour = list(button_colour)
        self._current_colour = self._button_colour
        self._outline_thickness = outline_thickness
        self._outline_colour = list(outline_colour)
        self._has_box = has_box
        self._has_outline = has_outline
        self._is_enabled = is_enabled

        self._is_hovering = False
        self._is_pressed = False
        self._rect = pygame.Rect(self._position, self._size)

    @property
    def click_func(self):
        return self._click_func

    @click_func.setter
    def click_func(self, value):
        if callable(value):
            self._click_func = value

    @property
    def click_sfx_id(self):
        return self._click_sfx_id

    @click_sfx_id.setter
    def click_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._click_sfx_id = value

    @property
    def hover_enter_sfx_id(self):
        return self._hover_enter_sfx_id

    @hover_enter_sfx_id.setter
    def hover_enter_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._hover_enter_sfx_id = value

    @property
    def hover_leave_sfx_id(self):
        return self._hover_leave_sfx_id

    @hover_leave_sfx_id.setter
    def hover_leave_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._hover_leave_sfx_id = value

    @property
    def disabled_click_sfx_id(self):
        return self._disabled_click_sfx_id

    @disabled_click_sfx_id.setter
    def disabled_click_sfx_id(self, value):
        if value in self._game.config["sfx_assets"].keys():
            self._disabled_click_sfx_id = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._size = list(value)
        else:
            raise TypeError

    @property
    def held_func(self):
        return self._held_func

    @held_func.setter
    def held_func(self, value):
        if callable(value):
            self._held_func = value

    @property
    def hover_leave_func(self):
        return self._hover_leave_func

    @hover_leave_func.setter
    def hover_leave_func(self, value):
        if callable(value):
            self._hover_leave_func = value

    @property
    def hover_enter_func(self):
        return self._hover_enter_func

    @hover_enter_func.setter
    def hover_enter_func(self, value):
        if callable(value):
            self._hover_enter_func = value

    @property
    def hover_colour(self):
        return self._hover_colour

    @hover_colour.setter
    def hover_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._hover_colour = value
            if self._is_hovering:
                self._current_colour = self._hover_colour

    @property
    def button_colour(self):
        return self._button_colour

    @button_colour.setter
    def button_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._button_colour = list(value)
            if not self._is_hovering:
                self._current_colour = self._button_colour

    @property
    def outline_thickness(self):
        return self._outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value):
        if type(value) is float or type(value) is int:
            self._outline_thickness = value

    @property
    def outline_colour(self):
        return self._outline_colour

    @outline_colour.setter
    def outline_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._outline_colour = value

    @property
    def is_hovering(self):
        return self._is_hovering

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
    def centre_position(self):
        return (self._position[0] + self._rect.size[0] / 2, self._position[1] + self._rect.size[1])

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._position = [value[0] - (self._size[0] / 2), value[1] - (self._size[1] / 2)]
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
