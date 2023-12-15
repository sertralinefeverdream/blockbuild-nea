class Region:
    def __init__(self, world, position):
        self._world = world
        self._position = position
        self._data = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def draw(self):
        for row_index, row in enumerate(self._data):
            for column_index, block in enumerate(row):
                if block is not None:
                    relative_pos_to_chunk_origin = (self._position + column_index * 40, self._position + row_index * 40)
                    absolute_pos = self._world.camera.get_screen_position(relative_pos_to_chunk_origin)
                    block.draw(absolute_pos)

    def update(self):
        for row in self._data:
            for block in row:
                if block is not None:
                    block.update()
