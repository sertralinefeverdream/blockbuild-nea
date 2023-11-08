import pygame


class AudioHandlerRefactored:

    game_vol= 0.6

    def __init__(self):
        pygame.mixer.init()
        self._library = {}

    def add_sfx_from_dict(self, sfx_dict):
        for sfx_id, sfx_path in sfx_dict.items():
            try:
                if sfx_id not in self._sfx_library.keys():
                    self._sfx_library[sfx_id] = pygame.mixer.Sound(sfx_path)
            except:
                print(f"{sfx_path} was invalid path!")

    def play_sfx(self, sfx_id):
        self._library[sfx_id].play()

    def stop_sfx(self, sfx_id):
        self._library[sfx_id].stop()

    def fadeout_sfx(self, sfx_id):
        self._library[sfx_id].fadeout()

    def update_volumes(self):
        for sfx in self._library.values():
            sfx.set_volume(AudioHandlerRefactored.game_vol)

