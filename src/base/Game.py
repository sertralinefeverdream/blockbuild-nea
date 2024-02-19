import sys
import pygame
from audio.Volume import Volume

#uploaded

class Game:
    def __init__(self, state_stack, window, clock, music_handler, sfx_handler, framerate, config, gui_factory,
                 block_factory, file_save_handler, item_factory, character_factory, item_container_factory,
                 spritesheet_factory, block_spritesheet, item_spritesheet):
        self._state_stack = state_stack
        self._window = window
        self._clock = clock
        self._music_handler = music_handler
        self._sfx_handler = sfx_handler
        self._framerate = framerate
        self._config = config
        self._gui_factory = gui_factory
        self._block_factory = block_factory
        self._file_save_handler = file_save_handler
        self._item_factory = item_factory
        self._character_factory = character_factory
        self._item_container_factory = item_container_factory
        self._spritesheet_factory = spritesheet_factory
        self._block_spritesheet = block_spritesheet
        self._item_spritesheet = item_spritesheet

        self._states = {}
        self._previous_state = None
        self._current_state = None
        self._running = True
        self._options = {
            "game_volume": Volume.MEDIUM,
            "music_volume": Volume.LOW
        }
        self._keys_pressed = []
        self._state_has_changed_flag = False

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
    def gui_factory(self):
        return self._gui_factory

    @property
    def block_factory(self):
        return self._block_factory

    @property
    def file_save_handler(self):
        return self._file_save_handler

    @property
    def item_factory(self):
        return self._item_factory

    @property
    def character_factory(self):
        return self._character_factory

    @property
    def item_container_factory(self):
        return self._item_container_factory

    @property
    def spritesheet_factory(self):
        return self._spritesheet_factory

    @property
    def block_spritesheet(self):
        return self._block_spritesheet

    @property
    def item_spritesheet(self):
        return self._item_spritesheet

    @property
    def states(self):
        return self._states

    @property
    def previous_state(self):
        return self._previous_state

    @property
    def current_state(self):
        return self._current_state

    @property
    def running(self):
        return self._running

    @property
    def keys_pressed(self):
        return self._keys_pressed

    def initialise_music_and_sfx(self):
        self._music_handler.add_music_from_dict(self._config["music_assets"])
        self._sfx_handler.add_sfx_from_dict(self._config["sfx_assets"])

    def game_loop(self):
        self.push_state("main_menu")
        self.update_states_from_option()

        for id, path in self._config["save_files"].items():
            self._file_save_handler.add_save_location(id, path)

        while self._running:
            self._keys_pressed = pygame.key.get_pressed()
            self._state_has_changed_flag = False
            # self.update_states_from_options() # Options can change during runtime. This method updates states in the game with whats set in the option dict as necessary.
            self._clock.tick(self._framerate)

            if self._current_state is not None:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    if event.type == pygame.USEREVENT + 1:  # Event id for whenever music stops playing.
                        self._music_handler.on_music_end()

                self._current_state.update()
                if self._current_state is not None and not self._state_has_changed_flag:
                    self._current_state.draw()
                    pygame.display.flip()
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

    def push_state(self, state_id, state_enter_params=None, state_leave_params=None):
        self._previous_state = self._state_stack.peek()
        print(f"LEAVING {self._state_stack.peek()}")
        self._state_stack.push(self._states[state_id.lower()])
        self._current_state = self._state_stack.peek()

        if self._previous_state is not None:
            self._previous_state.on_state_leave(state_leave_params)

        # print(f"PUSHING {self._current_state} TO THE STACK!")
        self._current_state.on_state_enter(state_enter_params)
        self._state_has_changed_flag = True

    def pop_state(self, state_enter_params=None, state_leave_params=None):
        self._previous_state = self._state_stack.pop()
        # print(f"POPPING {self._previous_state} OFF THE STACK!")
        self._current_state = self._state_stack.peek()

        self._previous_state.on_state_leave(state_leave_params)

        if self._current_state is not None:
            # print(f"ENTERING {self._current_state}")
            self._current_state.on_state_enter(state_enter_params)

        self._state_has_changed_flag = True

    def on_game_end(self):
        pygame.quit()
        sys.exit()
