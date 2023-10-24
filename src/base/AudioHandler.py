import warnings

import pygame
import random

'''
Audiohandler allows me to control the behaviour of playing sounds from one centralised part of my code instead of each
Game State having to implement their own code to play music.
'''


class AudioHandler:
    def __init__(self, music_fade_time, is_shuffling):
        pygame.mixer.init()
        self._sfx_library = {}  # Dictionary of sound ids and their respective sound objects
        self._music_library = {}  # Dictionary of music ids and their respective relative file paths.
        self._shuffle_list = []  # List of music ids that will be played at random when shuffle play is enabled.
        self._game_vol = 0
        self._music_vol = 0
        self._music_fade_time = music_fade_time
        self._is_shuffling = is_shuffling

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
        for sfx_id, sfx_path in sfx_dict.items():
            try:
                if sfx_id not in self._sfx_library.keys():
                    self._sfx_library[sfx_id] = pygame.mixer.Sound(sfx_path)
            except:
                print(f"{sfx_path} was invalid path!")

    def add_music_from_dict(self, music_dict):
        for music_id, music_path in music_dict.items():
            try:
                if music_id not in self._music_library.keys():
                    self._music_library[music_id] = music_path
            except:
                print(f"{music_path} was invalid path!")


    def set_shuffle_list(self, shuffle_list):
        self._shuffle_list = shuffle_list

    def play_music(self, music_id):
        self._is_shuffling = False
        if music_id in self._music_library.keys():
            pygame.mixer.music.load(self._music_library[music_id])
            pygame.mixer.music.play(fade_ms=self._music_fade_time)
        else:
            raise Exception

    def shuffle_play(self):
        self._is_shuffling = True
        if len(self._shuffle_list) != 0:
            pygame.mixer.music.load(self._music_library[random.choice(self._shuffle_list)])
            pygame.mixer.music.play(fade_ms=self._music_fade_time)
        else:
            print("Shuffle list empty!")

    def stop_music(self):
        self._is_shuffling = False
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def on_music_end(self):
        pygame.mixer.music.unload()
        if self._is_shuffling:
            self.shuffle_play()

    def play_sfx(self, sfx_name):
        self._sfx_library[sfx_name].play()

    def stop_sfx(self, sfx_name):
        self._sfx_library[sfx_name].stop()

    def fadeout_sfx(self, sfx_name):
        self._sfx_library[sfx_name].fadeout()

    def update_volumes(self):
        pygame.mixer.music.set_volume(self._music_vol)
        #print(self._game_vol)
        for sfx in self._sfx_library.values():
            sfx.set_volume(self._game_vol)
