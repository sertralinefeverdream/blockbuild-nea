import pygame.mixer


class SfxHandler:
    def __init__(self):
        pygame.mixer.init()
        self._sfx_library = {}

    def add_sfx_from_dict(self, sfx_dict):
        for sfx_id, sfx_path in sfx_dict.items():
            try:
                if sfx_id not in self._sfx_library.keys():
                    self._sfx_library[sfx_id] = pygame.mixer.Sound(sfx_path)
            except:
                print(f"{sfx_path} was invalid path!")

    def play_sfx(self, sfx_name):
        if sfx_name in self._sfx_library.keys():
            self._sfx_library[sfx_name].play()
