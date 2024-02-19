from sprite.Spritesheet import Spritesheet

#uploaded

class SpritesheetFactory:
    def __init__(self):
        pass

    def create_spritesheet(self, image_path, metadata_path):
        return Spritesheet(image_path, metadata_path)
