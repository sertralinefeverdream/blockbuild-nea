class World:
    def __init__(self, game, camera):
        self._game = game
        self._camera = camera
        self._data = {}

        self._regions_to_draw = []
        self._regions_to_update = []

    @property
    def camera(self):
        return self._camera

    @property
    def game(self):
        return self._game

    def update_draw_list(self):
        pass

    def update_update_list(self):
        pass

    def initialise_world(self, json_data=None):
        if json_data is None:
        else:
            # Code for converting json to actual data

    def update(self):
        self.update_update_list()
        for region in self._regions_to_update:
            region.update()
        self.update_draw_list()

    def draw(self):
        for region in self._regions_to_draw:
            region.draw()