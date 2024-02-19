import pygame.mixer
import random

#ADDED TO UPLOAD

class MusicHandler:
    def __init__(self, music_fade_time, is_shuffling):
        pygame.mixer.init()
        self._music_library = {}
        self._shuffle_list = []
        self._is_shuffling = is_shuffling
        self._music_fade_time = music_fade_time
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

    @property
    def music_library(self):
        return self._music_library

    @property
    def shuffle_list(self):
        return self._shuffle_list

    @property
    def is_shuffling(self):
        return self._shuffle_list

    @property
    def music_fade_time(self):
        return self._music_fade_time

    @music_fade_time.setter
    def music_fade_time(self, value):
        if type(value) is int and value >= 0:
            self._music_fade_time = value

    def set_shuffle_list(self, shuffle_list):
        self._shuffle_list = shuffle_list

    def shuffle_play(self):
        self._is_shuffling = True
        if len(self._shuffle_list) != 0:
            # print(self._music_library)
            pygame.mixer.music.load(self._music_library[random.choice(self._shuffle_list)])
            pygame.mixer.music.play(fade_ms=self._music_fade_time)
        else:
            print("Shuffle list empty!")

    def play_music(self, music_id):
        self._is_shuffling = False
        if music_id in self._music_library.keys():
            pygame.mixer.music.load(self._music_library[music_id])
            pygame.mixer.music.play(fade_ms=self._music_fade_time)
        else:
            raise Exception

    def stop_music(self):
        self._is_shuffling = False
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def add_music_from_dict(self, music_dict):
        for music_id, music_path in music_dict.items():
            self.add_music(music_id, music_path)

    def add_music(self, music_id, music_path):
        try:
            if music_id not in self._music_library.keys():
                self._music_library[music_id] = music_path
        except:
            print(f"{music_path} was invalid path!")

    def on_music_end(self):
        pygame.mixer.music.unload()
        if self._is_shuffling:
            self.shuffle_play()

    def update_volume(self, vol):
        pygame.mixer.music.set_volume(vol)
