import pygame
import os
import json

from states.MainMenuState import MainMenuState
from states.LoadGameMenuState import LoadGameMenuState
from states.OptionsMenuState import OptionsMenuState
from states.MainGameState import MainGameState
from states.PauseGameState import PauseGameState
from states.InventoryState import InventoryState
from states.ChestInteractState import ChestInteractState

from base.Game import Game
from base.FileSaveHandler import FileSaveHandler

from states.StateStack import StateStack

from factories.GUIFactory import GUIFactory
from factories.BlockFactory import BlockFactory
from factories.ItemFactory import ItemFactory
from factories.CharacterFactory import CharacterFactory
from factories.ItemContainerFactory import ItemContainerFactory
from factories.SpritesheetFactory import SpritesheetFactory

from world.Camera import Camera
from world.RegionGenerator import RegionGenerator
from world.World import World
from audio.MusicHandler import MusicHandler
from audio.SfxHandler import SfxHandler

#ADDED TO UPLOAD

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    config = None
    with open("config.json") as f:
        config = json.load(f)

    npc_spawn_data = config["generation_data"]["npc_spawn_data"]

    window = pygame.display.set_mode((config["window_size_x"], config["window_size_y"]))
    pygame.display.set_caption(config["window_caption"])

    state_stack = StateStack()
    clock = pygame.time.Clock()

    spritesheet_factory = SpritesheetFactory()
    gui_factory = GUIFactory()
    block_factory = BlockFactory(config["blocks"])
    item_factory = ItemFactory(config["items"])
    character_factory = CharacterFactory(config["characters"])
    item_container_factory = ItemContainerFactory()
    region_generator = RegionGenerator(generation_data=config["generation_data"])
    camera = Camera()
    file_save_handler = FileSaveHandler()

    block_spritesheet = spritesheet_factory.create_spritesheet(
        "../assets/imgs/sprites/block_textures/block_textures.png",
        "../assets/imgs/sprites/block_textures/block_textures.json")
    item_spritesheet = spritesheet_factory.create_spritesheet("../assets/imgs/sprites/item_textures/item_textures.png",
                                                              "../assets/imgs/sprites/item_textures/item_textures.json")

    music_handler = MusicHandler(250, False)
    sfx_handler = SfxHandler()
    game = Game(state_stack, window, clock, music_handler, sfx_handler, \
                config["framerate"], config, gui_factory, \
                block_factory, file_save_handler, item_factory, character_factory, item_container_factory,
                spritesheet_factory, block_spritesheet, item_spritesheet)  # Game class handles overall running of game
    game.add_to_states("main_menu", MainMenuState(game))
    game.add_to_states("options_menu", OptionsMenuState(game))
    game.add_to_states("load_game_menu", LoadGameMenuState(game))
    game.add_to_states("main_game", MainGameState(game, World(game, camera, region_generator,
                                                              npc_spawn_data["random_spawn_cooldown"],
                                                              npc_spawn_data["entity_spawn_limit_per_region"],
                                                              npc_spawn_data["entity_spawn_list"])))
    game.add_to_states("pause_game", PauseGameState(game))
    game.add_to_states("inventory", InventoryState(game))
    game.add_to_states("chest_interact", ChestInteractState(game))
    game.game_loop()


if __name__ == "__main__":
    main()
