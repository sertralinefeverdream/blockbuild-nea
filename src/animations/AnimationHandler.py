import pygame
#Added to upload

class AnimationHandler:
    def __init__(self, spritesheet):
        self._spritesheet = spritesheet
        self._animation_data = {}
        self._frame_timer = pygame.time.get_ticks()

        self._current_frame_pointer = 0
        self._current_animation_id = None
        self._loop = False
        self._reversed = False
        self._is_finished = True

    @property
    def current_animation_id(self):
        return self._current_animation_id

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value):
        if type(value) is bool:
            self._loop = value

    @property
    def reversed(self):
        return self._reversed

    @reversed.setter
    def reversed(self, value):
        if type(value) is bool:
            self._reversed = value

    @property
    def is_finished(self):
        return self._is_finished

    @property
    def current_frame(self):
        if self._current_animation_id is not None:
            # print(self._animation_data, self._current_animation_id, self._current_frame_pointer)
            current_frame = self._animation_data[self._current_animation_id][self._current_frame_pointer][0]
            if self._reversed:
                current_frame = pygame.transform.flip(current_frame, True, False)
            return current_frame

    def create_animation(self, animation_id, data):
        animation = []
        for sprite_parse_id, duration in data:
            animation.append((self._spritesheet.parse_sprite(sprite_parse_id), duration))
        self._animation_data[animation_id] = animation

    def play_animation_from_id(self, animation_id):
        if animation_id in self._animation_data.keys():
            self._current_frame_pointer = 0
            self._is_finished = False
            self._current_animation_id = animation_id
            self._frame_timer = pygame.time.get_ticks()

    def update(self):
        if self._current_animation_id is not None:
            if pygame.time.get_ticks() - self._frame_timer > \
                    self._animation_data[self._current_animation_id][self._current_frame_pointer][1]:
                self._frame_timer = pygame.time.get_ticks()
                if self._current_frame_pointer < len(self._animation_data[self._current_animation_id]) - 1:
                    self._current_frame_pointer += 1
                else:
                    if self._loop:
                        self._current_frame_pointer = 0
                    else:
                        self._is_finished = True

    def load_from_data(self, data):
        for animation_id, animation in data.items():
            self.create_animation(animation_id, animation)
