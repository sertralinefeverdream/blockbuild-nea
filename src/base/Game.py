class Game:
    def __init__(self, state_stack, window, clock):
        self.__state_stack = state_stack
        self.__window = window
        self.__clock = clock
        self.__states = {}
        self.__previous_state = None
        self.__current_state = None

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
        while True:
            self.__clock.tick(self.__current_state.max_framerate)
            self.__current_state.loop()

    def add_state(self, state_id, state):
        self.__states[state_id] = state


    def push_state(self, state_id):
        if state_id.lower() in self.__states.keys():
            self.__state_stack.push(self.__states[state_id.lower()])

    def pop_state(self):
        self.__previous_state = self.__state_stack.pop()


