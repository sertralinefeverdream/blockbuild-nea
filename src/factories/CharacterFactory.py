from src.entities.player.Player import Player

class CharacterFactory:
    def __init__(self, character_data):
        self._character_data = character_data

    def create_character(self, game, world, entity_id, size, texture, max_speed, max_health, state_data=None):
        if entity_id in self._character_data.keys():
            entity_data = self._character_data[entity_id]
            if entity_id == "player":
                entity = Player(game, world, entity_id, (0, 0), size, texture, max_speed)