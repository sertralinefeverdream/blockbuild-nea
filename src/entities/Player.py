from src.entities.CharacterBase import CharacterBase
import pygame

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, texture, max_speed, max_health):
        super().__init__(game, world, entity_id, position, size, texture, max_speed, max_health)

    def update(self):
        if self._health <= 0:
            self.kill()
            return

        deltatime = self._game.clock.get_time() / 1000

        self.handle_inputs(deltatime)

        self._velocity[1] += 600 # Gravity

        if abs(self._velocity[0]) > self._max_speed[0]:
            self._velocity[0] = self._max_speed[0] if self._velocity[0] > 0 else -self._max_speed[0]

        if abs(self._velocity[1]) > self._max_speed[1]:
            self._velocity[1] = self._max_speed[1] if self._velocity[1] > 0 else -self._max_speed[1]

        self._position[0] += self._velocity[0] * deltatime
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("horizontal")
        self._position[1] += self._velocity[1] * deltatime
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("vertical")

        '''
        self.handle_inputs()
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("horizontal")
        self._position[1] += self._velocity[1] * deltatime
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("vertical")
        '''

    def handle_inputs(self, deltatime):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_a]:
            if self._velocity[0] > 0:
                self._velocity[0] = 0
            self._velocity[0] += -10
        elif keys_pressed[pygame.K_d]:
            if self._velocity[0] < 0:
                self._velocity[0] = 0
            self._velocity[0] += 10
        else:
            self.velocity[0] *= 1/2

    def handle_collisions(self, axis):
        hitboxes_to_check = []

        for x in range(3):
            for y in range(3):
                region_check_x = self._position[0] + (x-1)*800
                region_check_y = self._position[1] + (y-1)*800

                if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                    hitboxes_to_check += self._world.get_region_at_position((region_check_x, region_check_y)).get_block_hitboxes()
                else:
                    print("Region invalid")

        if axis.lower() == "horizontal":
            for block, hitbox in hitboxes_to_check:
                if hitbox.colliderect(self._hitbox):
                    if self._velocity[0] > 0:
                        self._position[0] = block.position[0] - self._size[0]
                        self._velocity[0] = 0
                    elif self._velocity[0] < 0:
                        self._position[0] = block.position[0] + 40
                        self._velocity[0] = 0
                    self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)

        elif axis.lower() == "vertical":
            for block, hitbox in hitboxes_to_check:
                if hitbox.colliderect(self._hitbox):
                    if self._velocity[1] > 0:
                        self._position[1] = block.position[1] - self._size[1]
                        self._velocity[1] = 0
                    elif self._velocity[1] < 0:
                        self._position[1] = block.position[1] + 40
                        self._velocity[1] = 0
                    self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)

    def draw(self):
        #self._game.window.blit(self._texture, self._world.camera.get_screen_position(self._position))
        pygame.draw.rect(self._game.window, (255, 0, 0), self._hitbox)
        pygame.draw.rect(self._game.window, (0, 0, 0), pygame.Rect(self._world.camera.get_screen_position(self._position), self._size))