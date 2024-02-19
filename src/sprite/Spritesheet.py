import pygame
import json

#uploaded

class Spritesheet:
    def __init__(self, image_path, metadata_path):
        self._image = pygame.image.load(image_path).convert_alpha()

        with open(metadata_path) as f:
            self._metadata = json.load(f)

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self._image, (0, 0), (x, y, width, height))
        return sprite

    def parse_sprite(self, sprite_id):
        if sprite_id in self._metadata.keys():
            sprite_metadata = self._metadata[sprite_id]
            return self.get_sprite(sprite_metadata["x"], sprite_metadata["y"], sprite_metadata["width"],
                                   sprite_metadata["height"])
