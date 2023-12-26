import sys
import pygame
from src.audio.Volume import Volume

# Refactored


class Game:
    def __init__(self, state_stack, window, clock, music_handler, sfx_handler, framerate, config, gui_factory, block_factory):
        self._state_stack = state_stack
        self._window = window
        self._clock = clock
        self._music_handler = music_handler
        self._sfx_handler = sfx_handler
        self._framerate = framerate
        self._config = config
        self._gui_factory = gui_factory
        self._block_factory = block_factory

        self._states = {}
        self._keys_down = []
        self._previous_state = None
        self._current_state = None
        self._running = True
        self._options = {
            "game_volume": Volume.MEDIUM,
            "music_volume": Volume.LOW
        }

        self.initialise_music_and_sfx()

    @property
    def state_stack(self):
      return self._state_stack

    @property
    def window(self):
        return self._window

    @property
    def clock(self):
        return self._clock

    @property
    def music_handler(self):
        return self._music_handler

    @property
    def sfx_handler(self):
        return self._sfx_handler

    @property
    def config(self):
        return self._config

    @property
    def states(self):
        return self._states

    @property
    def keys_down(self):
        return self._keys_down

    @property
    def previous_state(self):
        return self._previous_state

    @property
    def current_state(self):
        return self._current_state

    @property
    def previous_state(self):
        return self._previous_state

    @property
    def running(self):
        return self._running

    @property
    def gui_factory(self):
        return self._gui_factory

    @property
    def block_factory(self):
        return self._block_factory

    def initialise_music_and_sfx(self):
        self._music_handler.add_music_from_dict(self._config["music_assets"])
        self._sfx_handler.add_sfx_from_dict(self._config["sfx_assets"])

    def game_loop(self):
        self.push_state("main_menu")
        self.push_state("main_game")
        self.update_states_from_option()

        while self._running:
            self._current_state = self._state_stack.peek()
            self._keys_down = pygame.key.get_pressed()
           # self.update_states_from_options() # Options can change during runtime. This method updates states in the game with whats set in the option dict as necessary.

            if self._current_state is not None:
                self._clock.tick(self._framerate)
                #print(self._clock.get_fps())

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    if event.type == pygame.USEREVENT + 1: # Event id for whenever music stops playing.
                        self._music_handler.on_music_end()

                self._current_state.update()
                pygame.display.update()
            else:
                self._running = False

        self.on_game_end()

    def get_option(self, option_index):
        return self._options[option_index]

    def set_option(self, option_index, value):
        self._options[option_index] = value
        self.update_states_from_option()

    def update_states_from_option(self):
        pygame.mixer.music.set_volume(self._options["music_volume"].value)

    def add_to_states(self, state_id, state):
        self._states[state_id] = state

    def push_state(self, state_id, *args):
        self._previous_state = self._state_stack.peek()
        self._state_stack.push(self._states[state_id.lower()], *args)

    def pop_state(self):
        self._previous_state = self._state_stack.pop()

    def on_game_end(self):
        pygame.quit()
        sys.exit()


