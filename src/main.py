import pygame
from config import config
from states.MainMenuState import MainMenuState
from states.LoadGameMenuState import LoadGameMenuState
from states.OptionsMenuState import OptionsMenuState

from base.Game import Game
from src.audio.MusicHandler import MusicHandler
from src.audio.AudioHandlerFactory import AudioHandlerFactory

from gui.GUIFactory import GUIFactory
from states.StateStack import StateStack

from src.base.SaveFileHandler import SaveFileHandler


def main():
    pygame.init()
    state_stack = StateStack()  # Holds different "states" which have their own game loops.
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((config["window_size_x"], config["window_size_y"]))
    music_handler = MusicHandler(20, False)
    save_file_handler = SaveFileHandler()
    gui_factory = GUIFactory()
    audio_handler_factory = AudioHandlerFactory()
    pygame.display.set_caption(config["window_caption"])
    game = Game(state_stack, window, clock, music_handler, save_file_handler, config["framerate"], config) # Game class handles overall running of game
    game.add_to_states("main_menu", MainMenuState(game, gui_factory, audio_handler_factory))
    game.add_to_states("options_menu", OptionsMenuState(game, gui_factory, audio_handler_factory))
    game.add_to_states("load_game_menu", LoadGameMenuState(game, gui_factory, audio_handler_factory))
    game.game_loop()

if __name__ == "__main__":
    print("Hello!")
    main()