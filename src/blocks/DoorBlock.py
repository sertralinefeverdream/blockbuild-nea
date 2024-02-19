import pygame

from blocks.InteractableBlockBase import InteractableBlockBase

#uploaded

class DoorBlock(InteractableBlockBase):
    def __init__(self, game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                 footstep_sfx_id, use_sfx_id, open_texture_id, closed_texture_id, loot_drop_id=None,
                 loot_drop_tool_whitelist=None, can_collide=True):
        super().__init__(game, world, position, hardness, block_id, texture, mine_sfx_id, place_and_break_sfx_id,
                         footstep_sfx_id, use_sfx_id, loot_drop_id, loot_drop_tool_whitelist, can_collide)
        self._open_texture_id = open_texture_id
        self._closed_texture_id = closed_texture_id

        self._current_state = "closed"
        self._redraw_flag = False

    def interact(self):
        self._game.sfx_handler.play_sfx(self._use_sfx_id, self._game.get_option("game_volume").value)

        self._current_state = "closed" if self._current_state == "open" else "open"
        self.update_door_states()

    def update_door_states(self):
        self._can_collide = False if self._current_state == "open" else True

        texture_id_to_parse = self._open_texture_id if self._current_state == "open" else self._closed_texture_id
        self._texture = pygame.transform.scale(self._game.block_spritesheet.parse_sprite(texture_id_to_parse), (40, 40))
        self.enable_flag_for_region_redraw()

    def update(self):
        if self._redraw_flag:
            if self._world.check_region_exists_at_position(self._position):
                self._world.get_region_at_position(self._position).enable_flag_for_redraw()
                self._redraw_flag = False

        screen_position = self._world.camera.get_screen_position(self._position)
        self._hitbox.update(screen_position, (40, 40))

    def enable_flag_for_region_redraw(self):
        self._redraw_flag = True

    def get_state_data(self):
        data = {}
        data["current_state"] = self._current_state
        return data

    def load_state_data(self, data):
        self._current_state = data["current_state"]
        self.update_door_states()
