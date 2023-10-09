from src.gui.ButtonBase import ButtonBase
import pygame


class TextButton(ButtonBase):
    def __init__(self, surface, pos_x, pos_y, size_x, size_y, click_func, text="Hello World", text_colour=(0, 0, 0), hover_colour=(127, 127, 127), button_colour=(0, 0, 0), outline_thickness=2, outline_colour = (0, 0, 0), is_toggle=False, is_enabled=True, is_visible=True):
        super().__init__(surface, pos_x, pos_y, size_x, size_y, click_func, hover_colour, button_colour, outline_thickness, outline_colour, is_enabled, is_visible)
        self._text_rect = None

    def on_hover_enter(self):
        pass

    def on_hover_leave(self):
        pass

    def on_mouse_click(self):
        pass

    def on_mouse_hold(self):
        pass

    def draw(self):
        pygame.draw.rect(self._surface, self._current_colour, self._rect)
        pygame.draw.rect(self._surface, self._outline_colour, self._rect, width=self._outline_thickness)

    def update(self):
        self._rect.update(self._pos_x, self._pos_y, self._size_x, self._size_y)