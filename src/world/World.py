import json


class World:
    def __init__(self, game, camera, region_generator):
        self._game = game
        self._camera = camera
        self._region_generator = region_generator

        self._player = None

        self._draw_list = []
        self._data = \
            {
                '0':
                    {
                        '0': self._region_generator.create_generated_region(self._game, self, (0, 0))
                    }
            }

    @property
    def game(self):
        return self._game

    @property
    def camera(self):
        return self._camera

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    @property
    def region_generator(self):
        return self._region_generator

    def reset(self):
        self._region_generator.randomise_seed()
        self._data.clear()
        self._draw_list.clear()
        self._data['0'] = {}
        self._data['0']['0'] = self._region_generator.create_generated_region(self._game, self, (0, 0))
        self._camera.x = 0
        self._camera.y = 0
        self._player = None

    def find_player_reference(self):
        for column in self._data.values():
            for region in column.values():
                for entity in region.entity_list:
                    if entity.entity_id == "player":
                        print("Player found")
                        return entity
        return None

    def update(self):
        if self._player is None:
            player_reference = self.find_player_reference()
            if player_reference is None:
                print("Player reference invalid")
                self._player = self._game.character_factory.create_character(self._game, self, "player")
                self.get_region_at_position((0, 0)).entity_list.append(self._player)
            else:
                self._player = player_reference

        self.update_draw_list()
        #print(self._draw_list)
        self.reassign_entities_to_regions()

        for x, y in self._draw_list:
            self._data[x][y].update()
            self._camera.x = self._player.position[0] - 600
            self._camera.y = self._player.position[1] - 400

    def draw(self):
        for x, y in self._draw_list:
            screen_position = self._camera.get_screen_position((int(x), int(y)))
            if (-800 <= screen_position[0] <= 1200) and (-800 <= screen_position[1] <= 800):
                self._data[x][y].draw_blocks()

        for x, y in self._draw_list:
            self._data[x][y].draw_entities()

    def get_region_indexes_from_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:

            x_index = int((position[0] // 800)) * 800
            y_index = int((position[1] // 800)) * 800

            return str(x_index), str(y_index)

    def check_region_exists_at_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            x_index, y_index = self.get_region_indexes_from_position(position)

            if x_index in self._data.keys():
                if y_index in self._data[x_index].keys():
                    return True
                else:
                    return False
            else:
                return False

    def get_region_at_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.check_region_exists_at_position(position):
                x_index, y_index = self.get_region_indexes_from_position(position)
                return self._data[x_index][y_index]
            else:
                print("Region no long exist")
                return None

    def get_block_at_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.check_region_exists_at_position(position):
                region = self.get_region_at_position(position)
                return region.get_block_at_position(position)

    def set_block_at_position(self, position, block_id, state_data=None):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.check_region_exists_at_position(position):
                region = self.get_region_at_position(position)
                region.set_block_at_position(position, block_id, state_data)

    def serialize(self):
        return json.dumps(self.convert_data())

    def load_from_serialized(self, data):
        self.load_from_data(json.loads(data))

    def convert_data(self):  # Converts classes to dict and array representations in preparation for json serialization
        data = {}
        for x_index, column in self._data.items():
            data[str(x_index)] = {}
            for y_index, region in column.items():
                data[str(x_index)][str(y_index)] = region.convert_data()
        return data

    def load_from_data(self, data):
        self.reset()
        for x_index, column in data.items():
            for y_index, region in column.items():
                if str(x_index) not in self._data.keys():
                    self._data[str(x_index)] = {}
                self._data[str(x_index)][str(y_index)] = self._region_generator.create_region_from_data(self._game, self, (
                    int(x_index), int(y_index)), region)

    def reassign_entities_to_regions(self): # Make sure entities are being updated by the region that they actually reside in.
        for region in [self.get_region_at_position((int(x), int(y))) for x, y in self._draw_list]:
            for entity in region.entity_list[::]:
                if not region.is_position_in_region(entity.position):
                    region_index_x, region_index_y = self.get_region_indexes_from_position(entity.position)
                    if self.check_region_exists_at_position(entity.position):
                        self._data[region_index_x][region_index_y].entity_list.append(entity)
                    region.entity_list.remove(entity)


    def update_draw_list(self): # Responsible for updating draw list and creating non-existent regions that need to be drawn
        self._draw_list.clear()
        camera_x = self._camera.x
        camera_y = self._camera.y

        for x in range(6):
            for y in range(6):
                region_check_x = camera_x + (x-3)*800
                region_check_y = camera_y + (y-3)*800

                region_index_x, region_index_y = self.get_region_indexes_from_position((region_check_x, region_check_y))

                region_exists = self.check_region_exists_at_position((region_check_x, region_check_y))

                if not region_exists:
                    # print("REGION DOESNT EXIST!")
                    if region_index_x not in self._data.keys():
                        self._data[region_index_x] = {}
                   # print("Generating new")
                    #self._data[region_index_x][region_index_y] = self._region_generator.create_region_from_data(self._game, self, (int(region_index_x), int(region_index_y)), self._default)
                    self._data[region_index_x][region_index_y] = self._region_generator.create_generated_region(self._game, self, (int(region_index_x), int(region_index_y)))
                self._draw_list.append((region_index_x, region_index_y))


