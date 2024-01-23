from src.sprite.Spritesheet import Spritesheet

class SpritesheetFactory:
    def __init__(self):
        pass

    def create_spritesheet(self, image_path, metadata_path):
        return Spritesheet(image_path, metadata_path)