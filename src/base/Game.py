import sys
import pygame


class Game:
    def __init__(self, state_stack, window, clock, framerate):
        self.__state_stack = state_stack
        self.__window = window
        self.__clock = clock
        self.__states = {}
        self.__previous_state = None
        self.__current_state = None
        self.__running = True

    '''
     @property
    def state_stack(self):
      return self.__state_stack
    '''

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
        self.__current_state = self.__state_stack.peek()
        while self.__running:
            if not self.__state_stack.empty():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__running = False

                self.__clock.tick(60)
                self.__current_state.loop()
                pygame.display.update()
            else:
                self.__running = False
        self.on_game_end()

    def on_game_end(self):
        print("Game ended")
        pygame.quit()
        sys.exit()

    def add_to_states(self, state_id, state):
        self.__states[state_id] = state

    def push_state(self, state_id):
        if state_id.lower() in self.__states.keys():
            self.__state_stack.push(self.__states[state_id.lower()])

    def pop_state(self):
        self.__previous_state = self.__state_stack.pop()


