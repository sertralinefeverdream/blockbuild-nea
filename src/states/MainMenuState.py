from src.states.StateBase import StateBase
from src.gui.TextButton import TextButton

class MainMenuState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._gui = {"test_button": TextButton(self.game.window, 600.0, 400.0, 75.0, 75.0, click_func=self.foo, outline_colour=(0, 0, 0), button_colour=(255, 0, 0))}

    def on_state_enter(self):
        print("Entered state!")

    def on_state_leave(self):
        print("Left state")

    def loop(self):
        self.game.window.fill((255, 255, 255))
        for component in self._gui.values():
           # self._gui["test_button"].position = (self._gui["test_button"].position[0] + 1.0, self._gui["test_button"].position[1])
            component.update()
            if component.is_visible:
                component.draw()

    def foo(self):
        pass