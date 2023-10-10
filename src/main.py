import pygame
import config
from states import MainMenuState, StateStack
from base import Game


def main():
    pygame.init()
    state_stack = StateStack.StateStack() # Holds different "states" which have their own game loops.
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((config.window_size_x, config.window_size_y))
    pygame.display.set_caption(config.window_caption)
    game = Game.Game(state_stack, window, clock, config.framerate) # Game class handles overall running of game
    game.add_to_states("main_menu", MainMenuState.MainMenuState(game))
    game.game_loop()


if __name__ == "__main__":
    main()