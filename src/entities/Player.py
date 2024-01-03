from src.entities.CharacterBase import CharacterBase
import pygame

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, texture, max_health):
        super().__init__(game, world, entity_id, position, size, texture, max_health)

    def update(self):
        self._velocity[1] += 1
        self.handle_inputs()
        self._position[0] += self._velocity[0]
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("horizontal")
        self._position[1] += self._velocity[1]
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("vertical")

    def handle_inputs(self):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_w]:
            if not self._is_jumping and not self._is_falling:
                self._velocity[1] = -18
                self._is_jumping = True

        if keys_pressed[pygame.K_a]:
            self._velocity[0] = -5
        elif keys_pressed[pygame.K_d]:
            self._velocity[0] = 5
        else:
            self._velocity[0] = 0

    def handle_collisions(self, axis):
        hitboxes_to_check = []

        for x in range(3):
            for y in range(3):
                region_check_x = self._position[0] + (x-1)*800
                region_check_y = self._position[1] + (y-1)*800

                if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                    hitboxes_to_check += self._world.get_region_at_position((region_check_x, region_check_y)).get_block_hitboxes()
                else:
                    pass

        if axis.lower() == "horizontal":
            for block, hitbox in hitboxes_to_check:
                if hitbox.colliderect(self._hitbox):
                    if self._velocity[0] > 0:
                        self._position[0] = block.position[0] - self._size[0]
                        self._velocity[0] = 0
                    elif self._velocity[0] < 0:
                        self._position[0] = block.position[0] + 40
                        self._velocity[0] = 0

        elif axis.lower() == "vertical":
            no_collision_below = True
            for block, hitbox in hitboxes_to_check:
                if hitbox.colliderect(self._hitbox):
                    if self._velocity[1] > 0:
                        self._position[1] = block.position[1] - self._size[1]
                        self._velocity[1] = 0
                        if self._is_jumping:
                            self._is_jumping = False
                        no_collision_below = False
                    elif self._velocity[1] < 0:
                        self._position[1] = block.position[1] + 40
                        self._velocity[1] = 0

            if no_collision_below:
                self._is_falling = True
            elif not no_collision_below:
                self._is_falling = False

        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)

    def draw(self):
        #self._game.window.blit(self._texture, self._world.camera.get_screen_position(self._position))
        pygame.draw.rect(self._game.window, (0, 0, 0), pygame.Rect(self._world.camera.get_screen_position(self._position), self._size))