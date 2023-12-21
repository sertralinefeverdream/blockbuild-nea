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

from src.blocks.BlockFactory import BlockFactory

from src.world.Camera import Camera
from src.world.RegionGenerator import RegionGenerator
from src.world.World import World

from states.MainGameState import MainGameState


def main():
    pygame.init()
    state_stack = StateStack()  # Holds different "states" which have their own game loops.
    clock = pygame.time.Clock()

    config = None
    with open("config.json") as f:
        config = json.load(f)

    window = pygame.display.set_mode((config["window_size_x"], config["window_size_y"]))
    pygame.display.set_caption(config["window_caption"])

    gui_factory = GUIFactory()
    audio_handler_factory = AudioHandlerFactory()
    block_factory = BlockFactory(config["blocks"], audio_handler_factory,
                                 Spritesheet("../assets/imgs/sprites/block_textures/block_textures.png",
                                             "../assets/imgs/sprites/block_textures/block_textures.json"))

    region_generator = RegionGenerator()
    camera = Camera()

    game = Game(state_stack, window, clock, audio_handler_factory.create_handler("musichandler", 250, False),
                config["framerate"], config, gui_factory, audio_handler_factory,
                block_factory)  # Game class handles overall running of game
    game.add_to_states("main_menu", MainMenuState(game))
    game.add_to_states("options_menu", OptionsMenuState(game))
    game.add_to_states("load_game_menu", LoadGameMenuState(game))
    game.add_to_states("main_game", MainGameState(game, World(game, camera, region_generator)))
    game.game_loop()


if __name__ == "__main__":
    main()

'''{
    '0': 
        {
            '0': <src.world.Region.Region object at 0x00000205373AA260>, 
            '-1600': <src.world.Region.Region object at 0x0000020537410CD0>
        }, 
    '-1600': 
        {
            '-1600': <src.world.Region.Region object at 0x00000205373E1F60>, 
            '0': <src.world.Region.Region object at 0x00000205373F5930>}, '-800': {'-1600': <src.world.Region.Region object at 
0x00000205373F5990>, '0': <src.world.Region.Region object at 0x00000205373FD330>}, '-2400': {'-1600': 
<src.world.Region.Region object at 0x0000020537423FD0>, '0': <src.world.Region.Region object at 0x00000205374340A0>}} 
'''
