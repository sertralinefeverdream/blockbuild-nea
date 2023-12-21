import json


class Region:
    def __init__(self, game, position=(0, 0)):
        self._game = game
        self._position = list(position)

        self._data = \
            [
                [None for x in range(20)] for y in range(20)
            ]  # Indexing for a block requires indexing y coordinate first

    @property
    def game(self):
        return self._game

    '''
     @property
    def world(self):
        return self._world
    '''

    def is_position_in_region(self, position):
        if self._position[0] <= position[0] < self._position[0] + 800 \
                and self._position[1] <= position[1] < self._position[1] + 800:
            return True
        else:
            return False

    def get_block_indexes_from_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.is_position_in_region(position):
                x_index = abs(position[0] - self._position[0]) // 40
                y_index = abs(position[1] - self._position[1]) // 40

                return x_index, y_index
            else:
                print("Block not in region!")

    def get_block_at_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.is_position_in_region(position):
                x_index, y_index = self.get_block_indexes_from_position(position)
                return self._data[y_index][x_index]

    def set_block_at_position(self, position, block_id, state_data=None):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.is_position_in_region(position):
                x_index, y_index = self.get_block_indexes_from_position(position)
                self._data[y_index][x_index] = self._game.block_factory.create_block(self._game, block_id, state_data)

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

    def draw(self, camera):
        for row_index, row in enumerate(self._data):
            for block_index, block in enumerate(row):
                if block is not None:
                    screen_position = camera.get_screen_position((
                        (self._position[0] + block_index * 40),
                        (self._position[1] + row_index * 40)
                    ))
                    if -40 < screen_position[0] < 1200 \
                            and -40 < screen_position[1] < 800:
                        block.draw(screen_position)

    def serialize(self):
        return json.dumps(self.convert_data())

    def load_from_serialized(self, data):
        self.load_from_data(json.loads(data))

    def convert_data(self):
        data = {str(x): [None for x in range(20)] for x in range(20)}
        for row_index, row in enumerate(self._data):
            for block_index, block in enumerate(row):
                if self._data[row_index][block_index] is not None:
                    data[str(row_index)][block_index] = self._data[row_index][block_index].convert_data()
                else:
                    data[str(row_index)][block_index] = None

        return data

    def load_from_data(self, data):
        # print(data)
        for row_index, row in data.items():
            for block_index, block in enumerate(row):
                if block is not None:
                    self._data[int(row_index)][block_index] = self._game.block_factory.create_block(self._game,
                                                                                                    block["block_id"],
                                                                                                    block["state_data"])
                # create_block is inefficient
                else:
                  #  print(row_index, block_index)
                    self._data[int(row_index)][block_index] = None
