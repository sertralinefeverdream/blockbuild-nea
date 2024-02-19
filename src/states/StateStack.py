#uploaded

class StateStack:
    def __init__(self):
        self.__stack = []

    def empty(self):
        return len(self.__stack) == 0

    def push(self, state):
        self.__stack.append(state)

    def pop(self):
        if not self.empty():
            temp = self.__stack[-1]
            del self.__stack[-1]
            return temp
        else:
            return None

    def peek(self):
        if not self.empty():
            return self.__stack[-1]
        else:
            return None
