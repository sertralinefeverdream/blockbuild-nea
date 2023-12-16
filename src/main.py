import pygame
import json

from states.MainMenuState import MainMenuState
from states.LoadGameMenuState import LoadGameMenuState
from states.OptionsMenuState import OptionsMenuState

from src.sprite.Spritesheet import Spritesheet

from base.Game import Game
from src.audio.AudioHandlerFactory import AudioHandlerFactory

from gui.GUIFactory import GUIFactory
from states.StateStack import StateStack

from src.blocks.legacy.BlockFactory import BlockFactory
from src.blocks.legacy.BlockBehaviourFactory import BlockBehaviourFactory

from states.MainGameState import MainGameState


def main():
    pygame.init()
    state_stack = StateStack()  # Holds different "states" which have their own game loops.
    clock = pygame.time.Clock()

    config = None
    with open("config.json") as f:
        config = json.load(f)

    window = pygame.display.set_mode((config["window_size_x"], config["window_size_y"]))

    gui_factory = GUIFactory()
    audio_handler_factory = AudioHandlerFactory()
    block_behaviour_factory = BlockBehaviourFactory(audio_handler_factory)
    block_factory = BlockFactory(config["blocks"], block_behaviour_factory, Spritesheet("../assets/imgs/sprites/block_textures/block_textures.png", "../assets/imgs/sprites/block_textures/block_textures.json"))

    pygame.display.set_caption(config["window_caption"])

    game = Game(state_stack, window, clock, audio_handler_factory.create_handler("musichandler", 250, False), config["framerate"], config, gui_factory, audio_handler_factory, block_factory) # Game class handles overall running of game
    game.add_to_states("main_menu", MainMenuState(game))
    game.add_to_states("options_menu", OptionsMenuState(game))
    game.add_to_states("load_game_menu", LoadGameMenuState(game))
    game.add_to_states("main_game", MainGameState(game))
    game.game_loop()


if __name__ == "__main__":
    main()