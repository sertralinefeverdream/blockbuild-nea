import pygame
from abc import ABC, abstractmethod
from src.gui.GUIBase import GUIBase


# Important! TextLabel is position from top-right position of the rendered font. Not its bounding box.

class TextLabel(GUIBase):
    def __init__(self, surface, position=(0, 0), box_overhang=(25, 25), box_colour=(255, 0, 0),
                 outline_thickness=5, outline_colour=(0, 0, 0), has_box=True, has_outline=True, is_visible=True, font_name="calibri",
                 font_size=50, text="BlockBuild!", text_colour=(0, 0, 0)):
        super().__init__(surface, position, is_visible)
        self._font_size = font_size
        self._font_name = font_name
        self._text = text
        self._text_colour = list(text_colour)
        self._outline_colour = list(outline_colour)
        self._outline_thickness = outline_thickness
        self._box_colour = list(box_colour)
        self._font = pygame.freetype.SysFont(font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour, size=self._font_size)
        self._has_box = has_box
        self._has_outline = has_outline
        self._box_overhang = list(box_overhang)
        self._box = pygame.Rect(
            (self._position[0] - self._box_overhang[0] / 2, self._position[1] - self._box_overhang[1] / 2),
            (self._rendered_font[1].size[0] + self._box_overhang[0], self._rendered_font[1].size[1] + self._box_overhang[1]))

        self.update_font()

    @property
    def outline_colour(self):
        return self._outline_colour

    @outline_colour.setter
    def outline_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._outline_colour = value

    @property
    def outline_thickness(self):
        return self._outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value):
        if type(value) is float or type(value) is int:
            self._outline_thickness = value

    @property
    def box_colour(self):
        return self._box_colour

    @box_colour.setter
    def box_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._box_colour = value

    @property
    def centre_position(self):
        return (self._position[0] + self._rendered_font[1].size[0] / 2, self._position[1] + self._rendered_font[1].size[1] / 2)

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._position = [value[0] - (self._rendered_font[1].size[0] / 2), value[1] - (self._rendered_font[1].size[1] / 2)]
        else:
            raise TypeError

    @property
    def has_box(self):
        return self._has_box

    @has_box.setter
    def has_box(self, value):
        if type(value) is bool:
            self._has_box = value

    @property
    def has_outline(self):
        return self._has_outline

    @has_outline.setter
    def has_outline(self, value):
        if type(value) is bool:
            self._has_outline = value

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self.update_font()

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, value):
        self._font_name = value
        self.update_font()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.update_font()

    @property
    def text_colour(self):
        return self._text_colour

    @text_colour.setter
    def text_colour(self, value):
        self._text_colour = value
        self.update_font()

    def conform_overhang_to_size(self, size): # Calculates overhang so that the box surrounding text conforms to a certain size
        if size[0] >= self._rendered_font[1].size[0] and size[1] >= self._rendered_font[1].size[1] and (type(size) is tuple or type(size is list)) and len(size) == 2:
            self._box_overhang[0] = (size[0] - self._rendered_font[1].size[0])
            self._box_overhang[1] = (size[1] - self._rendered_font[1].size[1])
            self.update_box()
            print(self._box.size)
        else:
            print("SIZE MUST BE LARGER THAN OR EQUAL TO SIZE OF ORIGINAL OR INVALID TYPE")

    def update_box(self):
        self._box.update((self._position[0] - self._box_overhang[0] / 2, self._position[1] - self._box_overhang[1] / 2),(
        self._rendered_font[1].size[0] + self._box_overhang[0], self._rendered_font[1].size[1] + self._box_overhang[1]))


    def update(self):
        self.update_box()

    def draw(self):
        if self._is_visible:
            if self._has_box:
                pygame.draw.rect(self._surface, self._box_colour, self._box)
            if self._has_outline:
                pygame.draw.rect(self._surface, self._outline_colour, self._box, width=self._outline_thickness)
            # self._surface.blit(self._rendered_font[0], (
            # self._position[0] + ((self._rect.size[0] - self._rendered_font[1].size[0]) / 2),
            # self._position[1] + ((self._rect.size[1] - self._rendered_font[1].size[1]) / 2)))
            self._surface.blit(self._rendered_font[0], self._position)

    def update_font(self):
        self._font = pygame.freetype.SysFont(self._font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour)
