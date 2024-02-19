from entities.Player import Player
from entities.GenericHostile import GenericHostile
from entities.GenericPassive import GenericPassive
from animations.AnimationHandler import AnimationHandler

#uploaded

class CharacterFactory:
    def __init__(self, character_data):
        self._character_data = character_data

    def create_character(self, game, world, entity_id, state_data=None):
        if entity_id in self._character_data.keys():
            entity_data = self._character_data[entity_id]
            entity_spritesheet = game.spritesheet_factory.create_spritesheet(entity_data["spritesheet_image_path"],
                                                                             entity_data["spritesheet_metadata_path"])
            animation_handler = AnimationHandler(entity_spritesheet)
            animation_handler.load_from_data(entity_data["animation_data"])
            entity = None
            if entity_data["type"] == "player":
                entity = Player(game, world, entity_id, (0, 0), entity_data["size"],
                                animation_handler=animation_handler, max_speed=entity_data["max_speed"],
                                max_health=entity_data["max_health"], hurt_sfx_id=entity_data["hurt_sfx_id"],
                                death_sfx_id=entity_data["death_sfx_id"])
            elif entity_data["type"] == "generic_hostile":
                print("MAKING GENERIC HOSTILE")
                entity = GenericHostile(game, world, entity_id, (0, 0), entity_data["size"],
                                        animation_handler=animation_handler, max_speed=entity_data["max_speed"],
                                        max_health=entity_data["max_health"],
                                        attack_damage=entity_data["attack_damage"],
                                        attack_range=entity_data["attack_range"],
                                        aggro_range=entity_data["aggro_range"], chase_range=entity_data["chase_range"],
                                        auto_jump_cooldown=entity_data["auto_jump_cooldown"],
                                        idle_cooldown=entity_data["idle_cooldown"],
                                        out_of_los_cooldown=entity_data["out_of_los_cooldown"],
                                        attack_cooldown=entity_data["attack_cooldown"],
                                        loot=entity_data["loot"],
                                        hurt_sfx_id=entity_data["hurt_sfx_id"],
                                        death_sfx_id=entity_data["death_sfx_id"],
                                        aggro_sfx_id=entity_data["aggro_sfx_id"],
                                        idle_sfx_id_list=entity_data["idle_sfx_id_list"],
                                        attack_sfx_id=entity_data["attack_sfx_id"],
                                        random_idle_sound_cooldown=entity_data["random_idle_sound_cooldown"]
                                        )
            elif entity_data["type"] == "generic_passive":
                entity = GenericPassive(game, world, entity_id, (0, 0), entity_data["size"],
                                        animation_handler=animation_handler,
                                        max_speed=entity_data["max_speed"], max_health=entity_data["max_health"],
                                        auto_jump_cooldown=entity_data["auto_jump_cooldown"],
                                        idle_cooldown=entity_data["idle_cooldown"], loot=entity_data["loot"],
                                        hurt_sfx_id=entity_data["hurt_sfx_id"],
                                        death_sfx_id=entity_data["death_sfx_id"],
                                        idle_sfx_id_list=entity_data["idle_sfx_id_list"],
                                        random_idle_sound_cooldown=entity_data["random_idle_sound_cooldown"],
                                        aggro_cooldown=entity_data["aggro_cooldown"])
            else:
                raise NotImplementedError

            if state_data is not None:
                entity.load_state_data(state_data)
            return entity
