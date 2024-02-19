from gui.ButtonBase import ButtonBase
import pygame
import pygame.freetype

#uploaded

class TextButton(ButtonBase):
    def __init__(self, game, surface, click_func, click_sfx_id="btn_click_1",
                 hover_enter_sfx_id="btn_hover_1", hover_leave_sfx_id=None, disabled_click_sfx_id="hello",
                 position=(0.0, 0.0), size=(100.0, 100.0), held_func=None, hover_leave_func=None, hover_enter_func=None,
                 hover_colour=(127, 0, 0), button_colour=(255, 0, 0), outline_thickness=5, outline_colour=(0, 0, 0),
                 has_box=True, has_outline=True,
                 is_enabled=True, is_visible=True, font_name="arial", font_size=50, text="Hello World",
                 text_colour=(0, 0, 0)):
        super().__init__(game, surface, click_func, click_sfx_id, hover_enter_sfx_id, hover_leave_sfx_id,
                         disabled_click_sfx_id, position, size, held_func, hover_leave_func, hover_enter_func,
                         hover_colour, button_colour, outline_thickness, outline_colour, has_box, has_outline,
                         is_enabled, is_visible)
        self._font_size = font_size
        self._font_name = font_name
        self._text = text
        self._text_colour = list(text_colour)

        self._font = pygame.freetype.SysFont(font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour, size=self._font_size)
        self._ticks = 0

        self.update_font()
        self.auto_resize_font()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        if type(value) is int:
            self._font_size = value
            self.update_font()
            self.auto_resize_font()

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, value):
        if type(value) is str:
            self._font_size = value
            self.update_font()
            self.auto_resize_font()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if type(value) is str:
            self._text = value
            self.update_font()
            self.auto_resize_font()

    @property
    def text_colour(self):
        return self._text_colour

    @text_colour.setter
    def text_colour(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 3:
            self._text_colour = value
            self.update_font()
            self.auto_resize_font()

    def auto_resize_font(self):
        while self._rendered_font[1].size[0] > self._size[0] or self._rendered_font[1].size[1] > self._size[1]:
            self._font_size -= 1
            self.update_font()

    def on_hover_enter(self):
        self._current_colour = self._hover_colour

        if self._hover_enter_sfx_id is not None:
            self._game.sfx_handler.play_sfx(self._hover_enter_sfx_id, self._game.get_option("game_volume").value)

        if self._is_enabled and self._hover_enter_func is not None:
            self._hover_enter_func()

    def on_hover_leave(self):
        self._current_colour = self._button_colour

        if self._hover_leave_sfx_id is not None:
            self._game.sfx_handler.play_sfx(self._hover_leave_sfx_id, self._game.get_option("game_volume").value)

        if self._is_enabled and self._hover_leave_func is not None:
            self._hover_leave_func()

    def on_mouse_click(self):
        if self.is_enabled:
            self._click_func(self)
            if self._click_sfx_id is not None:
                self._game.sfx_handler.play_sfx(self._click_sfx_id, self._game.get_option("game_volume").value)
        else:
            if self._disabled_click_sfx_id is not None:
                self._game.sfx_handler.play_sfx(self._disabled_click_sfx_id, self._game.get_option("game_volume").value)

    def on_mouse_hold(self):
        if self._is_enabled and self._held_func is not None:
            self._held_func(self)

    def update_font(self):
        self._font = pygame.freetype.SysFont(self._font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour)

    def draw(self):
        if self._is_visible:
            if self._has_box:
                pygame.draw.rect(self._surface, self._current_colour, self._rect)
            if self._has_outline:
                pygame.draw.rect(self._surface, self._outline_colour, self._rect, width=self._outline_thickness)
            self._surface.blit(self._rendered_font[0], (
                self._position[0] + ((self._size[0] - self._rendered_font[1].size[0]) / 2),
                self._position[1] + ((self._size[1] - self._rendered_font[1].size[1]) / 2)))

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
