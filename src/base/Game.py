import sys
import pygame
from src.audio.Volume import Volume


class Game:
    def __init__(self, state_stack, window, clock, music_handler, framerate, config):
        self.__state_stack = state_stack
        self.__config = config
        self.__window = window
        self.__music_handler = music_handler
        self.__clock = clock
        self.__framerate = framerate
        self.__states = {}
        self.__previous_state = None
        self.__current_state = None
        self.__running = True
        self.__options = {
            "game_volume": Volume.MEDIUM,
            "music_volume": Volume.MEDIUM
        }

        self.initialise_music()


    '''
     @property
    def state_stack(self):
      return self.__state_stack
    '''
    def initialise_music(self):
        pass

    @property
    def previous_state(self):
        return self.__previous_state

    @property
    def states(self):
        return self.__states

    @property
    def music_handler(self):
        return self.__music_handler

    @property
    def config(self):
        return self.__config

    @property
    def window(self):
        return self.__window

    @property
    def current_state(self):
        return self.__current_state

    @property
    def previous_state(self):
        return self.__previous_state

    @property
    def clock(self):
        return self.__clock

    def initialise_music(self):
        self.__music_handler.add_music_from_dict(
            {
                "main_menu": self.__config["music_assets"]["main_menu"]
            }
        )


    def game_loop(self):
        self.push_state("main_menu")

        while self.__running:
            self.__current_state = self.__state_stack.peek()
           # self.update_states_from_options() # Options can change during runtime. This method updates states in the game with whats set in the option dict as necessary.

            if self.__current_state is not None:
                self.__clock.tick(self.__framerate)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__running = False
                    if event.type == pygame.USEREVENT + 1: # Event id for whenever music stops playing.
                        self.__music_handler.on_music_end()

                self.__current_state.update()
                pygame.display.update()
            else:
                self.__running = False

        self.on_game_end()

    def on_game_end(self):
       # print("Game ended")
        pygame.quit()
        sys.exit()

    def add_to_states(self, state_id, state):
        self.__states[state_id] = state

    def get_option(self, option_index):
        return self.__options[option_index]

    def set_option(self, option_index, value):
        self.__options[option_index] = value

    def push_state(self, state_id):
        self.__previous_state = self.__state_stack.peek()
        self.__state_stack.push(self.__states[state_id.lower()])

    def pop_state(self):
        self.__previous_state = self.__state_stack.pop()
        return self.__previous_state


