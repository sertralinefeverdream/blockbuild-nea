import pygame
from abc import ABC, abstractmethod
from src.gui.GUIBase import GUIBase


class TextLabel(GUIBase):
    def __init__(self, surface, position=(0,0), size=(100, 100), box_colour=(0,0,0), outline_thickness=2, outline_colour=(0, 0, 0), has_box=True, is_visible=True, font_name="Calibri", font_size=50, text="BlockBuild!", text_colour=(0, 0, 0)):
        super().__init__(surface, position, size, is_visible)
        self._font_size = font_size
        self._font_name = font_name
        self._text = text
        self._text_colour = text_colour
        self._outline_colour = outline_colour
        self._outline_thickness = outline_thickness
        self._box_colour = box_colour
        self._font = pygame.freetype.SysFont(font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour, size=self._font_size)
        self._rect = pygame.Rect(self._position, self._size)
        self._has_box = has_box

    def update(self):
        pass

    def auto_resize_font(self):
        while self._rendered_font[1].size[0] > self._size[0] or self._rendered_font[1].size[1] > self._size[1]:
            self._font_size -= 1
            self.update_font()

    def draw(self):
        self.update_font()
        self.auto_resize_font()
        self._rect.update(self._position, self._size)

        if self._is_visible:
            if self._has_box:
                pygame.draw.rect(self._surface, self._box_colour, self._rect)
                pygame.draw.rect(self._surface, self._outline_colour, self._rect, width=self._outline_thickness)
            self._surface.blit(self._rendered_font[0], (self._position[0] + ((self._size[0] - self._rendered_font[1].size[0]) / 2),self._position[1] + ((self._size[1] - self._rendered_font[1].size[1]) / 2)))

    def update_font(self):
        self._font = pygame.freetype.SysFont(self._font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour)


    def update(self):
        self.update_font()
        self.auto_resize_font()
        self._rect.update(self._position, self._size)