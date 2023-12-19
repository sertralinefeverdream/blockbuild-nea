import json


class World:
    def __init__(self, game, region_generator):
        self._game = game
        self._camera = None
        self._region_generator = region_generator

        self._data = \
            {
                '0':
                    {
                        '0': self._region_generator.create_empty_region(self.game, (0, 0))
                    }
            }

    @property
    def game(self):
        return self._game

    @property
    def region_handler(self):
        return self._region_handler

    def update(self):
        for x_index, column in self._data.items():
            for y_index, region in column:
                region.update()

    def draw(self):
        for x_index, column in self._data.items():
            for y_index, region in column.items():
                region.draw()

    def serialize(self):  # Data must be converted first before serialization
        return json.dumps(self.convert_data())

    def convert_data(
            self):  # Converts classes to dict and array representations in preparation for serialization to json
        data = {}
        for x_index, column in self._data.items():
            data[str(x_index)] = {}
            for y_index, region in column.items():
                data[str(x_index)][str(y_index)] = region.convert_data()

        return data

    def load_from_data(self, data):
        for x_index, column in data.items():
            for y_index, region in column.items():
                self._data[str(x_index)][str(y_index)] = self._region_generator.create_region_from_data(self._game, (
                x_index, y_index), data[str(x_index)][str(y_index)])


    def load_from_serialized(self, data):
        self.load_from_data(json.loads(data))
