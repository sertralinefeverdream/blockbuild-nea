from gui.ButtonBase import ButtonBase
import pygame

#uploaded

class ItemButton(ButtonBase):
    def __init__(self, game, surface, click_func, click_sfx_id="btn_click_2", hover_enter_sfx_id=None,
                 hover_leave_sfx_id=None, disabled_click_sfx_id=None, position=(0.0, 0.0), size=(100, 100),
                 held_func=None, hover_leave_func=None, hover_enter_func=None, hover_colour=(255, 255, 255),
                 button_colour=(170, 170, 170), outline_thickness=5, outline_colour=(0, 0, 0), has_box=True,
                 has_outline=True, is_enabled=True,
                 is_visible=True, item_scale_multiplier=0.7, quantity_text_font="calibri", quantity_text_font_size=25,
                 quantity_text_font_colour=(0, 0, 0)):
        super().__init__(game, surface, click_func, click_sfx_id, hover_enter_sfx_id, hover_leave_sfx_id,
                         disabled_click_sfx_id, position,
                         size, held_func, hover_leave_func, hover_enter_func, hover_colour, button_colour,
                         outline_thickness, outline_colour, has_box, has_outline,
                         is_enabled, is_visible)
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
    def item_scale_multipler(self):
        return self._item_scale_multiplier

    @property
    def item_scale_multiplier(self, value):
        if type(value) is float and 0 < value <= 1:
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
        if (type(value) is list or type(value) is tuple) and len(value) == 3:
            self._quantity_text_font_colour = list(value)

    @property
    def quantity_text_font_size(self):
        return self._quantity_text_font_size

    @quantity_text_font_size.setter
    def quantity_text_font_size(self, value):
        if (type(value) is int or type(value) is float) and value > 0:
            self._quantity_text_font_size = value

    def update(self):
        self._rect.update(self._position, self._size)

        mouse_pos = pygame.mouse.get_pos()
        left_key_pressed = pygame.mouse.get_pressed()[0]

        if self._rect.collidepoint(mouse_pos):
            if not self._is_hovering:  # Changes states when it detects the cursor is hovering
                self._is_hovering = True
                self.on_hover_enter()

            if left_key_pressed:
                if not self._is_pressed:
                    self._is_pressed = True
                    self._ticks = pygame.time.get_ticks()  # Start counting how long the button has been held down for
                if pygame.time.get_ticks() - self._ticks > 200:  # If held down for more than 200 ticks assume held.
                    self.on_mouse_hold()  # Fires every tick
            else:
                if self._is_pressed:
                    self._is_pressed = False
                    self.on_mouse_click()  # Call click function when they stop pressing
        elif not self._rect.collidepoint(mouse_pos):
            if self._is_hovering:
                self._is_hovering = False
                self.on_hover_leave()
            if self._is_pressed:
                self._is_pressed = False

    def draw(self):
        if self._is_visible:
            if self._has_box:
                pygame.draw.rect(self._surface, self._current_colour, self._rect)
            if self._has_outline:
                pygame.draw.rect(self._surface, self._outline_colour, self._rect, width=self._outline_thickness)
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

    def on_mouse_hold(self):
        if self._is_enabled and self._held_func is not None:
            self._held_func(self)

    def on_mouse_click(self):
        if self.is_enabled:
            self._click_func(self)
            if self._click_sfx_id is not None:
                self._game.sfx_handler.play_sfx(self._click_sfx_id, self._game.get_option("game_volume").value)
        else:
            if self._disabled_click_sfx_id is not None:
                self._game.sfx_handler.play_sfx(self._disabled_click_sfx_id, self._game.get_option("game_volume").value)

    def on_hover_enter(self):
        self._current_colour = self._hover_colour

        if self._hover_enter_sfx_id is not None:
            self._game.sfx_handler.play_sfx(self._hover_enter_sfx_id, self._game.get_option("game_volume").value)

        if self._is_enabled and self._hover_enter_func is not None:
            self._hover_enter_func(self)

    def on_hover_leave(self):
        self._current_colour = self._button_colour
        if self._hover_leave_sfx_id is not None:
            self._game.sfx_handler.play_sfx(self._hover_leave_sfx_id, self._game.get_option("game_volume").value)

        if self._is_enabled and self._hover_leave_func is not None:
            self._hover_leave_func(self)
