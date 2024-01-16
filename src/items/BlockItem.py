import pygame
import math
from src.items.GenericItem import GenericItem

class BlockItem(GenericItem):
    def __init__(self, game, world, item_id, name, texture, quantity=-1, max_quantity=100, left_use_cooldown=100, right_use_cooldown=100, left_use_range=40, right_use_range=40, block_id="grass"):
        print(f'''DUN2PART {right_use_range} ''')
        super().__init__(game, world, item_id, name, texture, quantity, max_quantity, left_use_cooldown, right_use_cooldown, left_use_range, right_use_range)
        self._block_id = block_id
        print(f'''DUN4PART {self._right_use_range}''')

    def right_use(self, player_pos):
        mouse_pos = pygame.mouse.get_pos()
        world_pos_from_mouse = self._world.camera.get_world_position(mouse_pos)
        block_at_world_pos = self._world.get_block_at_position(world_pos_from_mouse)

        if math.sqrt((world_pos_from_mouse[0] - player_pos[0])**2 + (world_pos_from_mouse[1] - player_pos[1])**2) > self._right_use_range:
            print(f"Out of range {math.sqrt((world_pos_from_mouse[0] - player_pos[0])**2 + (world_pos_from_mouse[1] - player_pos[1])**2)}")
            return # return if outside of action range for right use action

        if block_at_world_pos is None and self._quantity != 0:
            entity_hitboxes_to_check = []
            block_pos = self._world.camera.get_screen_position(((world_pos_from_mouse[0]//40)*40, (world_pos_from_mouse[1]//40)*40))
            collision_check_rect = pygame.Rect(block_pos[0], block_pos[1], 40, 40)

            for x in range(6):
                for y in range(6):
                    region_check_x = world_pos_from_mouse[0] + (x-3)*800
                    region_check_y = world_pos_from_mouse[1] + (y-3)*800

                    if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                        entity_hitboxes_to_check += self._world.get_region_at_position((region_check_x, region_check_y)).get_entity_hitboxes()
                    else:
                        print("Region invalid for checking hitboxes")

            print(entity_hitboxes_to_check)
            for entity, hitbox in entity_hitboxes_to_check:
                if collision_check_rect.colliderect(hitbox):
                    print("Collision")
                    return # If entity in the way, the method will return and will not place the block

            self._world.set_block_at_position(world_pos_from_mouse, self._block_id)
            place_sfx_id = self._world.get_block_at_position(world_pos_from_mouse).place_sfx_id
            self._game.sfx_handler.play_sfx(place_sfx_id, self._game.get_option("game_volume").value)
            self._quantity -= 1


