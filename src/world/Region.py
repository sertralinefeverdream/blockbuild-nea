import json


class Region:
    def __init__(self, game, position=(0, 0)):
        self._game = game
        self._world_position = list(position)

        self._screen_position = self._world_position
        self._data = \
        [
            [None for x in range(30)] for y in range(30)
        ]

    @property
    def game(self):
        return self._game

    '''
     @property
    def world(self):
        return self._world
    '''


    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._position = list(value)

    def update(self):
        for row in self._data:
            for block in row:
                if block is not None:
                    block.update()

    def draw(self):
        for row_index, row in enumerate(self._data):
            for block_index, block in enumerate(row):
                if block is not None:
                    x = self._screen_position[0] + block_index*40
                    y = self._screen_position[1] + row_index*40
                    block.draw((x, y))


    def convert_data(self):
        data = {str(x): [None for x in range(30)] for x in range(30)}

        for row_index, row in enumerate(self._data):
            for block_index, block in enumerate(row):
                if self._data[row_index][block_index] is not None:
                    print(row_index, block_index)
                    data[str(row_index)][block_index] = self._data[row_index][block_index]
                else:
                    data[str(row_index)][block_index] = None

        return data

    def load_from_data(self, data):
        for row_index, row in data.items():
            for block_index, block in enumerate(row):
                if block is not None:
                    print(block["block_id"])
                    self._data[int(row_index)][block_index] = self._game.block_factory.create_block(self._game,
                                                                                                    block["block_id"],
                                                                                                    block["state_data"])
                else:
                    self._data[int(row_index)][block_index] = None
