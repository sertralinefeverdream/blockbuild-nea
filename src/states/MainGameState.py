from src.states.StateBase import StateBase
from src.world.Region import Region


class MainGameState(StateBase):
    def __init__(self, game):
        super().__init__(game)
        self._region = Region(self._game, world=None, position=(0, 0))
        print(self._region.serialize())
        self._region.load_from_serialized(
            '''{
            "0": [{"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null], "1": [{"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null], "2": [null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null], "3": [null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null], "4": [null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null], "5": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], 
            "6": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null], "7": [null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null], "8": [null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null], "9": [null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null], "10": [null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null], "11": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], 
            "12": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null], "13": [null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null], "14": [null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null], "15": [null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null], "16": [null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null], "17": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], 
            "18": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null], "19": [null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null], "20": [null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null], "21": [null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null], "22": [null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null], "23": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], 
            "24": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null], "25": [null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null], "26": [null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null], "27": [null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null], "28": [null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null], "29": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null]} '''
        )

    def initialise_gui(self):
        self._gui = [
            {},
            {},
            {}
        ]

    def on_state_enter(self):
        pass

    def on_state_leave(self):
        pass

    def update(self):
        self._game.window.fill((255, 255, 255))
        self._region.draw()
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()
