import json
import math
from src.entities.Player import Player

class World:
    def __init__(self, game, camera, region_generator):
        self._game = game
        self._camera = camera
        self._region_generator = region_generator

        self._player = Player(self._game, self, "Hi", (0, 0), (30, 30), None, [400, 400], 100)

        self._draw_list = []
        self._data = \
            {
                '0':
                    {
                        '0': self._region_generator.create_generated_region(self._game, self, (0, 0))
                    }
            }

        self._data['0']['0'].entity_list.append(self._player)

        #self._default = json.loads('''{"0": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "1": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "2": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "3": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "4": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "5": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "6": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "7": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "8": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "9": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "10": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "11": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "12": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "13": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "14": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "15": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null], "16": [null, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}], "17": [null, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}], "18": [null, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}], "19": [null, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}, {"block_id": "grass", "state_data": null}]}''')

    @property
    def game(self):
        return self._game

    @property
    def camera(self):
        return self._camera

    @property
    def region_generator(self):
        return self._region_generator

    def update(self):
        self.update_draw_list()
        #print(self._draw_list)
        self.reassign_entities_to_regions()

        for x, y in self._draw_list:
            self._data[x][y].update()
            self._camera.x = self._player.position[0] - 600
            self._camera.y = self._player.position[1] - 400

    def draw(self):
        self._game.window.fill((110, 177, 255))
        for x, y in self._draw_list:
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
        for x_index, column in data.items():
            for y_index, region in column.items():
                self._data[str(x_index)][str(y_index)] = self._region_generator.create_region_from_data(self._game, self, (
                    x_index, y_index), data[str(x_index)][str(y_index)])

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

        for x in range(7):
            for y in range(7):
                region_check_x = camera_x + (x-3)*800
                region_check_y = camera_y + (y-3)*800

                region_index_x, region_index_y = self.get_region_indexes_from_position((region_check_x, region_check_y))

                region_exists = self.check_region_exists_at_position((region_check_x, region_check_y))

                if not region_exists:
                    # print("REGION DOESNT EXIST!")
                    if region_index_x not in self._data.keys():
                        self._data[region_index_x] = {}
                    print("Generating new")
                    #self._data[region_index_x][region_index_y] = self._region_generator.create_region_from_data(self._game, self, (int(region_index_x), int(region_index_y)), self._default)
                    self._data[region_index_x][region_index_y] = self._region_generator.create_generated_region(self._game, self, (int(region_index_x), int(region_index_y)))
                self._draw_list.append((region_index_x, region_index_y))


