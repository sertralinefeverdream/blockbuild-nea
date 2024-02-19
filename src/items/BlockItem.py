import pygame
import math
from items.GenericItem import GenericItem

#uploaded


class BlockItem(GenericItem):
    def __init__(self, game, world, item_id, name, texture, quantity=1, max_quantity=100, attack_cooldown=100,
                 use_cooldown=100, attack_range=40, use_range=40, attack_strength=10, default_mine_strength=10,
                 preferred_mine_strength=40, preferred_mine_strength_white_list=None, block_id="grass"):
        super().__init__(game, world, item_id, name, texture, quantity, max_quantity, attack_cooldown, use_cooldown,
                         attack_range, use_range, attack_strength, default_mine_strength, preferred_mine_strength,
                         preferred_mine_strength_white_list)
        self._block_id = block_id

    def right_use(self, player_pos):
        mouse_pos = pygame.mouse.get_pos()
        mouse_world_pos = self._world.camera.get_world_position(mouse_pos)
        block_at_world_pos = self._world.get_block_at_position(mouse_world_pos)

        if math.sqrt((mouse_world_pos[0] - player_pos[0]) ** 2 + (
                mouse_world_pos[1] - player_pos[1]) ** 2) > self._use_range:
            return  # return if outside of action range for right use action

        if block_at_world_pos is None and self._quantity != 0:
            entity_hitboxes_to_check = []
            block_pos = self._world.camera.get_screen_position(
                ((mouse_world_pos[0] // 40) * 40, (mouse_world_pos[1] // 40) * 40))
            collision_check_rect = pygame.Rect(block_pos[0], block_pos[1], 40, 40)

            for x in range(6):
                for y in range(6):
                    region_check_x = mouse_world_pos[0] + (x - 3) * 800
                    region_check_y = mouse_world_pos[1] + (y - 3) * 800

                    if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                        entity_hitboxes_to_check += self._world.get_region_at_position(
                            (region_check_x, region_check_y)).get_entity_hitboxes()
                    else:
                        print("Region invalid for checking hitboxes")

            # print(entity_hitboxes_to_check)
            for entity, hitbox in entity_hitboxes_to_check:
                if collision_check_rect.colliderect(hitbox):
                    print("Collision")
                    return  # If entity in the way, the method will return and will not place the block

            self._world.set_block_at_position(mouse_world_pos, self._block_id)
            place_and_break_sfx_id = self._world.get_block_at_position(mouse_world_pos).place_and_break_sfx_id
            self._game.sfx_handler.play_sfx(place_and_break_sfx_id, self._game.get_option("game_volume").value)
            self._quantity -= 1
