from src.entities.CharacterBase import CharacterBase
import pygame

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, texture, max_health):
        super().__init__(game, world, entity_id, position, size, texture, max_health)

    def update(self):
        pass

    def handle_inputs(self):
        pass

    def handle_collisions(self): # Called after updating velocities i guess
        pass

    def draw(self):
        pass

