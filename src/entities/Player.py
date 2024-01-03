from src.entities.CharacterBase import CharacterBase
import pygame

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, texture, max_health):
        super().__init__(game, world, entity_id, position, size, texture, max_health)

    def update(self):
        self.handle_inputs()
        self._position[0] += self._velocity[0]
        self._position[1] += self._velocity[1]

    def handle_inputs(self):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_w]:
            self._velocity[1] = -5
        elif keys_pressed[pygame.K_s]:
            self._velocity[1] = 5
        else:
            self._velocity[1] = 0

        if keys_pressed[pygame.K_a]:
            self._velocity[0] = -5
        elif keys_pressed[pygame.K_d]:
            self._velocity[0] = 5
        else:
            self._velocity[0] = 0

    def handle_collisions(self, axis):
        if axis.lower() == "horizontal":
            pass
        elif axis.lower() == "vertical":
            pass

    def draw(self):
        pygame.draw.rect(self._game.window, (0, 0, 0), self._hitbox)