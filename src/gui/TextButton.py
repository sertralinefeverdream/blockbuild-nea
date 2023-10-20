from src.gui.ButtonBase import ButtonBase
import pygame
import pygame.freetype


class TextButton(ButtonBase):
    def __init__(self, surface, click_func, position=(0.0, 0.0), size=(50.0, 50.0),  held_func=None, hover_leave_func=None, hover_enter_func=None, hover_colour=(127,127,127), button_colour=(0,0,0), outline_thickness=2, outline_colour=(0, 0, 0), is_enabled=True, is_visible=True, font_name="Arial", font_size=50, text="Hello World", text_colour=(0, 0, 0)):
        super().__init__(surface, click_func, position, size, held_func, hover_leave_func, hover_enter_func, hover_colour, button_colour, outline_thickness, outline_colour, is_enabled, is_visible)
        self._font_size = font_size
        self._font_name = font_name
        self._text = text
        self._text_colour = text_colour
        self._font = pygame.freetype.SysFont(font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour, size=self._font_size)
        self.__ticks = 0

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, value):
        self._font_size = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_colour(self):
        return self._text_colour

    @text_colour.setter
    def text_colour(self, value):
        self._text_colour = value

    def auto_resize_font(self):
        while self._rendered_font[1].size[0] > self._size[0] or self._rendered_font[1].size[1] > self._size[1]:
            self._font_size -= 1
            self.update_font()

    def on_hover_enter(self):
        self._current_colour = self._hover_colour

    def on_hover_leave(self):
        self._current_colour = self._button_colour

    def on_mouse_click(self):
        if self.is_enabled:
            self._click_func(self)

    def on_mouse_hold(self):
        if self._held_func is not None and self._is_enabled:
            self._held_func(self)

    def update_font(self):
        self._font = pygame.freetype.SysFont(self._font_name, self._font_size)
        self._rendered_font = self._font.render(self._text, fgcolor=self._text_colour)

    def draw(self):
        if self._is_visible:
            pygame.draw.rect(self._surface, self._current_colour, self._rect)
            pygame.draw.rect(self._surface, self._outline_colour, self._rect, width=self._outline_thickness)
            self._surface.blit(self._rendered_font[0], (self._position[0] + ((self._size[0] - self._rendered_font[1].size[0]) / 2), self._position[1] + ((self._size[1] - self._rendered_font[1].size[1]) / 2)))
    def update(self):
        self.update_font()
        self.auto_resize_font()
        self._rect.update(self._position, self._size)
        #print(self.centre_position)

        mouse_pos = pygame.mouse.get_pos()
        left_key_pressed = pygame.mouse.get_pressed()[0]

        if self._rect.collidepoint(mouse_pos):
            if not self._is_hovering:  # Changes states when it detects the cursor is hovering
                self._is_hovering = True
                self.on_hover_enter()

            if left_key_pressed:
                if not self._is_pressed:
                    self._is_pressed = True
                    self.__ticks = pygame.time.get_ticks()  # Start counting how long the button has been held down for
                if pygame.time.get_ticks() - self.__ticks > 200:  # If held down for more than 200 ticks assume held.
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


