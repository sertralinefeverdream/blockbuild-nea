import pygame
import random


class AudioHandler:
    def __init__(self, music_fade_time, is_music_auto_play):
        pygame.mixer.init()
        self._sfx_library = {}
        self._music_library = {}
        self._music_list = []
        self._game_vol = 0
        self._music_vol = 0
        self._music_fade_time = music_fade_time
        self._is_music_auto_play = is_music_auto_play

        pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
        self.update_volumes()

    @property
    def game_vol(self):
        return self._game_vol

    @game_vol.setter
    def game_vol(self, value):
        if 1 >= value >= 0:
            self._game_vol = value
            self.update_volumes()
        else:
            raise ValueError

    @property
    def music_vol(self):
        return self._music_vol

    @music_vol.setter
    def music_vol(self, value):
        if 1 >= value >= 0:
            self._music_vol = value
            self.update_volumes()
        else:
            raise ValueError

    def add_sfx_from_dict(self, sfx_dict):
        for sfx_name, sfx_path in sfx_dict.items():
            try:
                if sfx_name not in self._sfx_library.keys():
                    self._sfx_library[sfx_name] = pygame.mixer.Sound(sfx_path)
                    print(sfx_name)
            except:
                print(f"{sfx_path} was invalid path!")

    def add_music_from_dict(self, music_dict):
        for music_name, music_path in music_dict.items():
            try:
                if music_name not in self._music_library.keys():
                    self._music_library[music_name] = music_path
            except:
                pass
       # print(self._music_library)

    def set_music_list(self, music_list):
        self._music_list = music_list

    def play_from_music_list(self, music_name):
        pygame.mixer.music.load(self._music_library[music_name])
        pygame.mixer.music.play(fade_ms=self._music_fade_time)

    def stop_music_list(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def on_music_end(self):
        pygame.mixer.music.unload()
        if self._is_music_auto_play:
            self.play_from_music_list(random.choice(self._music_list))

    def play_sfx(self, sfx_name):
        self._sfx_library[sfx_name].play()

    def stop_sfx(self, sfx_name):
        self._sfx_library[sfx_name].stop()

    def fadeout_sfx(self, sfx_name):
        self._sfx_library[sfx_name].fadeout()

    def update_volumes(self):
        for sfx in self._sfx_library.values():
            sfx.set_volume(self._game_vol)

        pygame.mixer.music.set_volume(self._music_vol)

