import json
import math

class Region:
    def __init__(self, game, world, position=(0, 0)):
        self._game = game
        self._world = world
        self._position = list(position)

        self._data = \
            [
                [None for x in range(20)] for y in range(20)
            ]  # Indexing for a block requires indexing y coordinate

        self._entity_list = []

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

    @property
    def entity_list(self):
        return self._entity_list

    @entity_list.setter
    def entity_list(self, value):
        if type(value) is list:
            self._entity_list = value

    @position.setter
    def position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._position = list(value)

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

    def get_block_at_indexes(self, x, y):
        if (type(x) is int and type(y) is int) and 0 <= x <= 20 and 0 <= y <= 20:
            return self._data[y][x]

    def set_block_at_position(self, position, block_id, state_data=None):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.is_position_in_region(position):
                x_index, y_index = self.get_block_indexes_from_position(position)
                self._data[y_index][x_index] = self._game.block_factory.create_block(self._game, self._world, (self._position[0] + x_index*40, self._position[1] + y_index*40), block_id, state_data)

    def set_block_at_indexes(self, x, y, block_id, state_data=None):
        if (type(x) is int and type(y) is int) and 0 <= x <= 20 and 0 <= y <= 20:
            self._data[y][x] = self._game.block_factory.create_block(self._game, self._world, (self._position[0] + x*40, self._position[1] + y*40), block_id, state_data)

    def get_block_hitboxes(self):
        data = []
        for row in self._data:
            for block in row:
                if block is not None:
                    data.append((block, block.hitbox))
        return data

    def update(self):
        for row in self._data:
            for block in row:
                if block is not None:
                    if block.is_broken:
                        del block
                    else:
                        block.update()

        for entity in self._entity_list:
            if entity.is_killed:
                self._entity_list.remove(entity)
                del entity
                continue
            entity.update()

    def draw_blocks(self):
        for row_index, row in enumerate(self._data):
            for block_index, block in enumerate(row):
                if block is not None:
                    screen_position = self._world.camera.get_screen_position((
                        (self._position[0] + block_index * 40),
                        (self._position[1] + row_index * 40)
                    ))
                    if -40 < screen_position[0] < 1200 \
                            and -40 < screen_position[1] < 800:
                        block.draw()

    def draw_entities(self):
        for entity in self._entity_list:
            entity.draw()

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
                    self._data[int(row_index)][block_index] = self._game.block_factory.create_block(self._game, self._world,
                                                                                                    (self._position[0] + block_index*40, self._position[1] + int(row_index)*40),
                                                                                                    block["block_id"],
                                                                                                    block["state_data"])
                else:
                    self._data[int(row_index)][block_index] = None
