import pygame.mixer

#UPLOADED

class SfxHandler:
    def __init__(self):
        pygame.mixer.init()
        self._sfx_library = {}

    @property
    def sfx_library(self):
        return self._sfx_library

    def add_sfx_from_dict(self, sfx_dict):
        for sfx_id, sfx_path in sfx_dict.items():
            self.add_sfx(sfx_id, sfx_path)

    def add_sfx(self, sfx_id, sfx_path):
        try:
            if sfx_id not in self._sfx_library.keys():
                self._sfx_library[sfx_id] = pygame.mixer.Sound(sfx_path)
        except:
            print(f"{sfx_path} was invalid path!")

    def play_sfx(self, sfx_id, vol):
        if sfx_id in self._sfx_library.keys():
            if 0 <= vol <= 1:
                self._sfx_library[sfx_id].set_volume(vol)
            self._sfx_library[sfx_id].play()

    def stop_sfx(self, sfx_id):
        if sfx_id in self._sfx_library.keys():
            self._sfx_library[sfx_id].stop()
