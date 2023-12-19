class World:
    def __init__(self, game, camera):
        self._game = game
        self._camera = camera
        self._data = {'0'}

    @property
    def camera(self):
        return self._camera

    @property
    def game(self):
        return self._game

    def update(self):
        pass

    def draw(self):
        pass

    def serialize(self):
        pass

    def load_from_serialized(self, data):
        pass