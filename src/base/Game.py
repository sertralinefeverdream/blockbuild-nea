import sys
import pygame
from src.audio.Volume import Volume

# Refactored


class Game:
    def __init__(self, state_stack, window, clock, music_handler, sfx_handler, framerate, config, gui_factory, block_factory, file_save_handler):
        self.__state_stack = state_stack
        self.__window = window
        self.__clock = clock
        self.__music_handler = music_handler
        self.__sfx_handler = sfx_handler
        self.__framerate = framerate
        self.__config = config
        self._gui_factory = gui_factory
        self._block_factory = block_factory
        self._file_save_handler = file_save_handler

        self.__states = {}
        self.__previous_state = None
        self.__current_state = None
        self.__running = True
        self.__options = {
            "game_volume": Volume.MEDIUM,
            "music_volume": Volume.LOW
        }
        self._keys_pressed = []

        self.initialise_music_and_sfx()

    @property
    def state_stack(self):
      return self.__state_stack

    @property
    def window(self):
        return self.__window

    @property
    def clock(self):
        return self.__clock

    @property
    def music_handler(self):
        return self.__music_handler

    @property
    def sfx_handler(self):
        return self.__sfx_handler

    @property
    def config(self):
        return self.__config

    @property
    def states(self):
        return self.__states

    @property
    def previous_state(self):
        return self.__previous_state

    @property
    def current_state(self):
        return self.__current_state

    @property
    def previous_state(self):
        return self.__previous_state

    @property
    def running(self):
        return self.__running

    @property
    def gui_factory(self):
        return self._gui_factory

    @property
    def block_factory(self):
        return self._block_factory

    @property
    def file_save_handler(self):
        pass

    @property
    def keys_pressed(self):
        return self._keys_pressed

    def initialise_music_and_sfx(self):
        self.__music_handler.add_music_from_dict(self.__config["music_assets"])
        self.__sfx_handler.add_sfx_from_dict(self.__config["sfx_assets"])

    def game_loop(self):
        self.push_state("main_menu")
        self.update_states_from_option()

        while self.__running:
            self.__current_state = self.__state_stack.peek()
            self._keys_pressed = pygame.key.get_pressed()
           # self.update_states_from_options() # Options can change during runtime. This method updates states in the game with whats set in the option dict as necessary.
            self.__clock.tick(self.__framerate)

            if self.__current_state is not None:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__running = False
                    if event.type == pygame.USEREVENT + 1: # Event id for whenever music stops playing.
                        self.__music_handler.on_music_end()

                self.__current_state.update()
                if self.__current_state is not None:
                    self.__current_state.draw()
                    pygame.display.flip()
            else:
                self.__running = False

        self.on_game_end()

    def get_option(self, option_index):
        return self.__options[option_index]

    def set_option(self, option_index, value):
        self.__options[option_index] = value
        self.update_states_from_option()

    def update_states_from_option(self):
        pygame.mixer.music.set_volume(self.__options["music_volume"].value)

    def add_to_states(self, state_id, state):
        self.__states[state_id] = state

    def push_state(self, state_id, state_enter_params=None, state_leave_params=None):
        self.__previous_state = self.__state_stack.peek()
        self.__state_stack.push(self.__states[state_id.lower()], state_enter_params, state_leave_params)
        self.__current_state = self.__state_stack.peek()

    def pop_state(self, state_enter_params=None, state_leave_params=None):
        self.__previous_state = self.__state_stack.pop(state_enter_params, state_leave_params)
        self.__current_state = self.__state_stack.peek()

    def on_game_end(self):
        pygame.quit()
        sys.exit()


