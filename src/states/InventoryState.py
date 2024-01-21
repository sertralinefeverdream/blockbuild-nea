from src.states.StateBase import StateBase

class InventoryState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._inventory = None
        self._hotbar = None
        self._inventory_key_held = False
        self._current_item = None

    def initialise_gui(self):
        self._gui = {}

    def on_state_enter(self, params):
        self._inventory = params[0]
        self._hotbar = params[1]

        for layer in self._gui[::-1]:
            for component in layer.values():
                component.update()

    def on_state_leave(self, params):
        pass

    def update(self):
        if self._game.keys_pressed[pygame.K_e]:
            self._inventory_key_held = True
        elif not self._game.keys_pressed[pygame.K_e] and self._inventory_key_held:
            self._game.pop_state()
            self._inventory_key_held = False

    def draw(self):
        self._game.states["main_game_"].draw(True)

