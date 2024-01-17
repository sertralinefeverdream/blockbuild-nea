import pygame

class AnimationHandler:
    def __init__(self, spritesheet):
        self._spritesheet = spritesheet
        self._animation_data = {}
        self._frame_timer = pygame.time.get_ticks()

        self._current_frame_pointer = 0
        self._current_animation_id = "idle"
        self._loop = False
        self._reversed = False

    @property
    def current_frame(self):
        if self._current_animation_id is not None:
            return self._animation_data[self._current_animation_id][self._current_frame_pointer][0]

    @property
    def reversed(self):
        return self._reversed

    @reversed.setter
    def reversed(self , value):
        if type(value) is bool:
            self._reversed = value

    def create_animation(self, animation_id, data):
        animation = []
        for sprite_parse_id, duration in data:
            animation.append((self._spritesheet.parse_sprite(sprite_parse_id), duration))
        self._animation_data[animation_id] = animation

    def play_animation_from_id(self, animation_id):
        self._current_frame_pointer = 0
        self._current_animation_id = animation_id

    def load_from_data(self, data):
        for animation_id, animation in data.items():
            self.create_animation(animation_id, animation)

    def update(self):
        if pygame.time.get_ticks() - self._frame_timer > self._animation_data[self._current_animation_id][self._current_frame_pointer][1]:
            self._frame_timer = pygame.time.get_ticks()
            self._current_frame_pointer += 1
            if self._current_frame_pointer > len(self._animation_data[self._current_animation_id]) - 1:
                if not self._loop:
                    self.play_animation_from_id("idle")
                else:
                    self._current_frame_pointer = 0





