import pygame
import config
from states import MainMenuState, StateStack, OptionsMenuState, LoadGameMenuState
from base import Game, AudioHandler
from gui.GUIFactory import GUIFactory


def main():
    pygame.init()
    state_stack = StateStack.StateStack()  # Holds different "states" which have their own game loops.
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((config.config["window_size_x"], config.config["window_size_y"]))
    audiohandler = AudioHandler.AudioHandler(500, False)
    gui_factory = GUIFactory()
    pygame.display.set_caption(config.config["window_caption"])
    game = Game.Game(state_stack, window, clock, audiohandler, config.config["sfx_assets"], config.config["music_assets"], config.config["framerate"], config.config) # Game class handles overall running of game
    game.add_to_states("main_menu", MainMenuState.MainMenuState(game, gui_factory))
    game.add_to_states("options_menu", OptionsMenuState.OptionsMenuState(game, gui_factory))
    game.add_to_states("load_game_menu", LoadGameMenuState.LoadGameMenuState(game, gui_factory))
    game.game_loop()


if __name__ == "__main__":
    main()