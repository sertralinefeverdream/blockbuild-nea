from src.entities.CharacterBase import CharacterBase
import pygame

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, texture, max_health):
        super().__init__(game, world, entity_id, position, size, texture, max_health)

    def update(self):
        self.handle_inputs()
        self.handle_horizontal_collisions()
        self._position[0] += self._velocity[0]
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_vertical_collisions()
        self._position[1] += self._velocity[1]
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)

    def handle_inputs(self):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_w]:
            self._velocity[1] = -1
        elif keys_pressed[pygame.K_s]:
            self._velocity[1] = 1
        else:
            self._velocity[1] = 0

        if keys_pressed[pygame.K_a]:
            self._velocity[0] = -1
        elif keys_pressed[pygame.K_d]:
            self._velocity[0] = 1
        else:
            self._velocity[0] = 0

    def handle_collisions(self): # Called after updating velocities i guess
        regions_to_check = [(self._position[0] + (x-1)*800, self._position[1]) for x in range(3)]
        regions_to_check += [(self._position[0], self._position[1] + (y - 1) * 800) for y in range(3)]
        hitboxes_to_check = []

        for (x_index, y_index) in regions_to_check:
            print(x_index, y_index)
            hitboxes_to_check += self._world.get_region_at_position((x_index, y_index)).get_block_hitboxes()

        for block, hitbox in hitboxes_to_check:
            if hitbox.colliderect(self._hitbox):
                pass


    def draw(self):
        pygame.draw.rect(self._game.window, (0, 0, 0), self._hitbox)