from gui.RectBox import RectBox
import pygame

#uploaded

class ItemDisplay(RectBox):
    def __init__(self, game, surface, position=(0, 0), is_visible=True, size=(100.0, 100.0), box_colour=(200, 200, 200),
                 outline_thickness=5, outline_colour=(0, 0, 0), has_box=True, has_outline=True,
                 item_scale_multiplier=0.7, quantity_text_font="calibri", quantity_text_font_size=25,
                 quantity_text_font_colour=(0, 0, 0)):
        super().__init__(game, surface, position, is_visible, size, box_colour, outline_thickness, outline_colour,
                         has_box, has_outline)
        self._item = None
        self._item_scale_multiplier = item_scale_multiplier
        self._quantity_text_font = quantity_text_font
        self._quantity_text_font_colour = list(quantity_text_font_colour)
        self._quantity_text_font_size = quantity_text_font_size

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self._item = value

    @property
    def item_scale_multiplier(self):
        return self._item_scale_multiplier

    @item_scale_multiplier.setter
    def item_scale_multiplier(self, value):
        if type(value) is float and 0 <= value <= 1:
            self._item_scale_multiplier = value

    @property
    def quantity_text_font(self):
        return self._quantity_text_font

    @quantity_text_font.setter
    def quantity_text_font(self, value):
        if type(value) is str:
            self._quantity_text_font = value

    @property
    def quantity_text_font_colour(self):
        return self._quantity_text_font_colour

    @quantity_text_font_colour.setter
    def quantity_text_font_colour(self, value):
        if (type(value) is list or type(value) is int) and len(value) == 3:
            self.quantity_text_font_colour = list(value)

    @property
    def quantity_text_font_size(self):
        return self._quantity_text_font_size

    @quantity_text_font_size.setter
    def quantity_text_font_size(self, value):
        if type(value) is int and value > 1:
            self._quantity_text_font_size = value

    def update(self):
        self._box.update(self._position, self._size)

    def draw(self):
        if self._is_visible:
            if self._has_box:
                pygame.draw.rect(self._surface, self._box_colour, self._box)
            if self._has_outline:
                pygame.draw.rect(self._surface, self._outline_colour, self._box, width=self._outline_thickness)

            if self._item is not None:
                quantity_text = pygame.freetype.SysFont(self._quantity_text_font, self._quantity_text_font_size).render(
                    f"{self._item.quantity if not hasattr(self._item, '''durability''') else self._item.durability}",
                    fgcolor=self._quantity_text_font_colour)
                item_texture = pygame.transform.scale(self._item.texture, (
                self._size[0] * self._item_scale_multiplier, self._size[1] * self._item_scale_multiplier))
                self._surface.blit(item_texture, (
                self._position[0] + (self._size[0] - self._size[0] * self._item_scale_multiplier) / 2,
                self._position[1] + (self._size[0] - self._size[0] * self._item_scale_multiplier) / 2))
                self._surface.blit(quantity_text[0], (
                self._position[0] + self._outline_thickness, self._position[1] + self._outline_thickness))
