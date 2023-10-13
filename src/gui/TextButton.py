from src.gui.ButtonBase import ButtonBase
import pygame
import pygame.freetype


class TextButton(ButtonBase):
    def __init__(self, surface, pos_x, pos_y, size_x, size_y, click_func, held_func=None, offset_x=0, offset_y=0, font_name="Arial", font_size=50, text="Hello World", text_colour=(0, 0, 0), hover_colour=(127, 127, 127), button_colour=(0, 0, 0), outline_thickness=2, outline_colour = (0, 0, 0), is_enabled=True, is_visible=True):
        super().__init__(surface, pos_x, pos_y, size_x, size_y, click_func, held_func, hover_colour, button_colour, outline_thickness, outline_colour, is_enabled, is_visible)
        self._font_size = font_size
        self._font_name = font_name
        self._text = text
        self._text_colour = text_colour
        self._font = pygame.freetype.SysFont(font_name, self._font_size)
        self._font_rect = None
        self._offset_x = offset_x
        self._offset_y = offset_y
        self.__ticks = 0

        self.update_font()

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
        self._font_size = value
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

    @property
    def offset(self):
        return (self._offset_x, self._offset_y)

    @offset.setter
    def offset(self, value):
        if (type(value) is tuple or type(value) is list) and len(value) == 2 and type(value[0]) is float and type(value[1]) is float:
            self._offset_x, self._offset_y = value
            self.update_font()
        else:
            raise TypeError

    def on_hover_enter(self):
        self._current_colour = self._hover_colour

    def on_hover_leave(self):
        self._current_colour = self._button_colour

    def on_mouse_click(self):
        self._click_func(self)

    def on_mouse_hold(self):
        if self._held_func is not None:
            self._held_func(self)

    def update_font(self):
        self._font = pygame.freetype.SysFont(self._font_name, self._font_size)
        self._font.size = (self._size_x/3, self._size_y/3)
        print("updated font")

    def draw(self):
        pygame.draw.rect(self._surface, self._current_colour, self._rect)
        pygame.draw.rect(self._surface, self._outline_colour, self._rect, width=self._outline_thickness)
        self._font.render_to(self._surface, (self._pos_x, self._pos_y), self._text, self._text_colour)

    def update(self):
        self._rect.update(self._pos_x, self._pos_y, self._size_x, self._size_y)

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
                print("Returned")
                self._is_hovering = False
                self.on_hover_leave()
            if self._is_pressed:
                self._is_pressed = False


