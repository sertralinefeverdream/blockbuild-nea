from src.entities.player.Player import Player
from src.sprite.Spritesheet import Spritesheet
from src.animations.AnimationHandler import AnimationHandler

class CharacterFactory:
    def __init__(self, character_data):
        self._character_data = character_data

    def create_character(self, game, world, entity_id, state_data=None):
        if entity_id in self._character_data.keys():
            entity_data = self._character_data[entity_id]
            entity_spritesheet = Spritesheet(entity_data["spritesheet_image_path"], entity_data["spritesheet_metadata_path"])
            animation_handler = AnimationHandler(entity_spritesheet)
            animation_handler.load_from_data(entity_data["animation_data"])
            entity = Player(game, world, entity_id, (0, 0), entity_data["size"], animation_handler=animation_handler, max_speed=entity_data["max_speed"], max_health=entity_data["max_health"])
            if state_data is not None:
                entity.load_state_data(state_data)
            return entity


