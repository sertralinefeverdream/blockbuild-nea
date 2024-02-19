from gui.GUIBase import GUIBase
import pygame

#uploaded


class RectBox(GUIBase):
    def __init__(self, game, surface, position=(0, 0), is_visible=True, size=(100.0, 100.0), box_colour=(255, 0, 0),
                 outline_thickness=5, outline_colour=(0, 0, 0), has_box=True, has_outline=True):
        super().__init__(game, surface, position, is_visible)
        self._size = list(size)
        self._box_colour = list(box_colour)
        self._outline_thickness = outline_thickness
        self._outline_colour = list(outline_colour)
        self._has_box = has_box
        self._has_outline = has_outline
        self._box = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])

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
    def box_colour(self):
        return self._box_colour

    @box_colour.setter
    def box_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._box_colour = list(value)

    @property
    def outline_thickness(self):
        return self._outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value):
        if type(value) is int and value > 0:
            self._outline_thickness = value

    @property
    def outline_colour(self):
        return self._outline_colour

    @outline_colour.setter
    def outline_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._outline_colour = list(value)

    @property
    def outline_thickness(self):
        return self._outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value):
        if type(value) is float or type(value) is int:
            self._outline_thickness = value

    @property
    def centre_position(self):
        return (self._position[0] + self._size[0] / 2, self._position[1] + self._size[1] / 2)

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2:
            self._position = [value[0] - (self._size[0] / 2), value[1] - (self._size[1] / 2)]
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

    def update(self):
        self._box.update(self._position, self._size)

    def draw(self):
        if self._is_visible:
            if self._has_box:
                pygame.draw.rect(self._surface, self._box_colour, self._box)
            if self._has_outline:
                pygame.draw.rect(self._surface, self._outline_colour, self._box, width=self._outline_thickness)
