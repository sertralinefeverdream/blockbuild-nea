'''
StateStack is a stack which handles which Game State (StateBase child class) instance is ran.
Each StateBase child class has its own function which is called every frame update.
Whatever object is at the top of the stack, its update method is called and drawn.
When a state is pushed or popped off the stack, whatever the current state is has its
on_state_leave method is called the state that is now on the top of the stack has its on_state_enter method
drawn.
This allows for behaviour to be encoded whenever a state is left or entered i.e. perhaps saving a game file, etc
'''


class StateStack:
    def __init__(self):
        self.__stack = []

    def empty(self):
        return len(self.__stack) == 0

    def push(self, state, *args):
        if not self.empty():
            self.__stack[-1].on_state_leave(*args)

        self.__stack.append(state)
        state.on_state_enter()

    def pop(self, *args):
        if not self.empty():
            temp = self.__stack[-1]
            temp.on_state_leave()
            del self.__stack[-1]
            if not self.empty():
                self.__stack[-1].on_state_enter(*args)
            return temp
        else:
            return None

    def peek(self):
        if not self.empty():
            return self.__stack[-1]
        else:
            return None

