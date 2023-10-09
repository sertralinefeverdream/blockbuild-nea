from src.states.StateBase import StateBase

class MainMenuState(StateBase):
    def __init__(self, game, max_framerate):
        super().__init__(game, max_framerate)

    def on_state_enter(self):
        print("Entered state!")

    def on_state_leave(self):
        print("Left state")

    def loop(self):
        print("Hello welt!")