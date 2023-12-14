import pygame


class Block:
    def __init__(self, game, block_behaviour, texture):
        self._game = game
        self._block_behaviour = block_behaviour
        self._texture = pygame.transform.scale(pygame.image.load(texture), (120, 120))

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if type(value) is pygame.Surface:
            self._texture = pygame.transform.scale(value, (120, 120))

    @property
    def block_behaviour(self):
        return self._block_behaviour

    @block_behaviour.setter
    def block_behaviour(self, value):
        self._block_behaviour = value


    def update(self):
        if self._block_behaviour is not None:
            self._block_behaviour.update()
        else:
            raise NotImplementedError

    def draw(self, screen_position):
        if self._block_behaviour is not None:
            self._game.window.blit(self._texture, screen_position)
        else:
            raise NotImplementedError
