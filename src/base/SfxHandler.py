import pygame.mixer


class SfxHandler:
    def __init__(self, game, sound_ids):
        pygame.mixer.init()
        self._game = game
        self._sounds = {}

    def add_sound(self, sound_id):
        sound_config = self._game.config["sfx_assets"]
        if sound_id not in self._sounds.keys() and sound_id in sound_config.keys():
            self._sounds[sound_id] = pygame.mixer.Sound(sound_config[sound_id])

    def play_sound(self, sound_id):
        if sound_id in self._sounds.keys():
            self._sounds[sound_id].play()

    def stop_sound(self, sound_id):
        if sound_id in self._sounds.keys():
            self._sounds[sound_id].stop()