from src.animations.AnimationHandler import AnimationHandler
import json

class AnimationHandlerFactory:
    def __init__(self):
        pass

    def create_animation_handler(self, spritesheet, animation_data_path=None):
        animation_handler = AnimationHandler(spritesheet)
        if animation_data_path is not None:
            with open(animation_data_path, "r") as f:
                animation_handler.load_from_data(json.load(f))
        return animation_handler
