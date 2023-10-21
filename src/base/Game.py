import sys
import pygame


class Game:
    def __init__(self, state_stack, window, clock, audiohandler, framerate, config):
        self.__state_stack = state_stack
        self.__config = config
        self.__window = window
        self.__clock = clock
        self.__audiohandler = audiohandler
        self.__framerate = framerate
        self.__states = {}
        self.__previous_state = None
        self.__current_state = None
        self.__running = True
        self.__options = {
            "game_volume":"medium",
            "music_volume":"medium"
        }

    '''
     @property
    def state_stack(self):
      return self.__state_stack
    '''

    @property
    def previous_state(self):
        return self.__previous_state

    @property
    def states(self):
        return self.__states

    @property
    def audiohandler(self):
        return self.__audiohandler

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

    def game_loop(self):
        self.push_state("main_menu")

        while self.__running:
            self.__audiohandler.game_vol = 0.9 if self.__options["game_volume"] == "high" else 0.6 if self.__options["game_volume"] == "medium" else 0.3
            self.__audiohandler.music_vol = 0.7 if self.__options["music_volume"] == "high" else 0.4 if self.__options["music_volume"] == "medium" else 0.1

            if not self.__state_stack.empty():
                self.__current_state = self.__state_stack.peek()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__running = False
                    if event.type == pygame.USEREVENT + 1:
                        self.__audiohandler.on_music_end()

                self.__clock.tick(self.__framerate)
                self.__current_state.loop()
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


