import pygame.mixer


class SfxHandler:
    def __init__(self, game):
        pygame.mixer.init()
        self._game = game
        self._sfx_library = {}

    def add_sfx_from_dict(self, sfx_dict):
        for sfx_id, sfx_path in sfx_dict.items():
            self.add_sfx(sfx_id, sfx_path)

    def add_sfx(self, sfx_id, sfx_path):
        try:
            if sfx_id not in self._sfx_library.keys():
                self._sfx_library[sfx_id] = pygame.mixer.Sound(sfx_path)
        except:
            print(f"{sfx_path} was invalid path!")

    def play_sfx(self, sfx_id, vol=0.6):
        if sfx_id in self._sfx_library.keys():
            if vol is not None and 0 <= vol.value <= 1:
                self._sfx_library[sfx_id].set_volume(vol)
            self._sfx_library[sfx_id].play()

    def stop_sfx(self, sfx_id):
        if sfx_id in self._sfx_library.keys():
            self._sfx_library[sfx_id].stop()

