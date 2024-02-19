import pygame
from gui.ButtonBase import ButtonBase

#uploaded

class ImageButton(ButtonBase):
    def __init__(self, game, surface, click_func, click_sfx_id=None, hover_enter_sfx_id=None, hover_leave_sfx_id=None,
                 disabled_click_sfx_id=None, position=(0.0, 0.0), size=(100, 100), held_func=None,
                 hover_leave_func=None, hover_enter_func=None, hover_colour=(127, 0, 0), button_colour=(255, 0, 0),
                 outline_thickness=5, outline_colour=(0, 0, 0), has_box=True, has_outline=True, is_enabled=True,
                 is_visible=True, image_scale_multiplier=1.0):
        super().__init__(game, surface, click_func, click_sfx_id, hover_enter_sfx_id, hover_leave_sfx_id,
                         disabled_click_sfx_id, position, size, held_func, hover_leave_func, hover_enter_func,
                         hover_colour, button_colour, outline_thickness, outline_colour, has_box, has_outline,
                         is_enabled, is_visible)
        self._image = None
        self._image_scale_multiplier = image_scale_multiplier

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if type(value) is pygame.Surface or type(value) is None:
            self._image = value

    @property
    def image_scale_multiplier(self):
        return self._image_scale_multiplier

    @image_scale_multiplier.setter
    def image_scale_multiplier(self, value):
        if type(value) is float and 0.0 < value < 1.0:
            self._image_scale_multiplier = value

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
            if self._image is not None:
                self._surface.blit(pygame.transform.scale(self._image, (
                self._size[0] * self._image_scale_multiplier, self._size[1] * self._image_scale_multiplier)), (
                                   self._position[0] + self._size[0] / 2 - (
                                               self._size[0] * self._image_scale_multiplier) / 2,
                                   self._position[1] + self._size[1] / 2 - (
                                               self._size[1] * self._image_scale_multiplier) / 2))

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
