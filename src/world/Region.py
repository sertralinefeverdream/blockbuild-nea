import pygame
import random

#uploaded

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
        self._region_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
        self._flag_for_redraw = True

    @property
    def game(self):
        return self._game

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

    def update(self):
        # print(f"REGION DEPTH: {len(self._data)}, REGION WIDTH: {len(self._data[0])}")
        for row in self._data:
            for x_index, block in enumerate(row):
                if block is not None:
                    if block.is_broken:
                        row[x_index] = None
                        del block
                        self.enable_flag_for_redraw()
                    else:
                        block.update()

        for entity in self._entity_list:
            entity.update()

        for entity in self._entity_list:
            if entity.is_killed:
                self.remove_entity(entity)
                del entity

    def draw_blocks(self):
        if self._flag_for_redraw:
            # print("Redrawing")
            self._flag_for_redraw = False
            self._region_surface.fill((110, 177, 255))
            for row_index, row in enumerate(self._data):
                for block_index, block in enumerate(row):
                    if block is not None:
                        self._region_surface.blit(block.texture, (block_index * 40, row_index * 40))

        self._game.window.blit(self._region_surface, self._world.camera.get_screen_position(self._position))

    def draw_entities(self):
        for entity in self._entity_list:
            entity.draw()

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

                if x_index < 0:
                    x_index = 0
                elif x_index > 19:
                    x_index = 19

                if y_index < 0:
                    y_index = 0
                elif y_index > 19:
                    y_index = 19

                return int(x_index), int(y_index)
            else:
                print("Block not in region!")

    def position_from_block_indexes(self, block_indexes):
        if 0 <= block_indexes[0] <= 19 and 0 <= block_indexes[1] <= 19:
            return self._position[0] + block_indexes[0] * 40, self._position[1] + block

    def get_quantity_of_blocks_in_region(self, block_id):
        total = 0
        for row in self._data:
            for block in row:
                if block is not None and block_id is not None:
                    if block.block_id == block_id:
                        total += 1
                elif block is None and block_id is None:
                    total += 1
        return total

    def get_random_block_of_type_by_id(self, block_id):  # Get a random block of type "block_id" within the region
        random_block = None
        if self.get_quantity_of_blocks_in_region(block_id) > 0:
            blocks_of_same_type_list = []
            for row in self._data:
                for block in row:
                    if block is not None:
                        if block.block_id == block_id:
                            blocks_of_same_type_list.append(block)
            random_block = random.choice(blocks_of_same_type_list)
        return random_block

    def get_block_at_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.is_position_in_region(position):
                x_index, y_index = self.get_block_indexes_from_position(position)
                # print(position)
                # print(x_index, y_index)
                return self._data[y_index][x_index]

    def get_block_at_indexes(self, x, y):
        if (type(x) is int and type(y) is int) and 0 <= x <= 20 and 0 <= y <= 20:
            return self._data[y][x]

    def set_block_at_position(self, position, block_id, state_data=None):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            if self.is_position_in_region(position):
                self.enable_flag_for_redraw()
                x_index, y_index = self.get_block_indexes_from_position(position)
                self._data[y_index][x_index] = self._game.block_factory.create_block(self._game, self._world, (
                    self._position[0] + x_index * 40, self._position[1] + y_index * 40), block_id, state_data)

    def set_block_at_indexes(self, x, y, block_id, state_data=None):
        if (type(x) is int and type(y) is int) and 0 <= x <= 20 and 0 <= y <= 20:
            self._data[y][x] = self._game.block_factory.create_block(self._game, self._world, (
                self._position[0] + x * 40, self._position[1] + y * 40), block_id, state_data)

    def get_block_hitboxes(self):
        data = []
        for row in self._data:
            for block in row:
                if block is not None:
                    data.append((block, block.hitbox))
        return data

    def get_entity_hitboxes(self):
        data = []
        for entity in self._entity_list:
            data.append((entity, entity.hitbox))
        return data

    def get_entities_at_position(self, position, ignore_player=True):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            list_of_entities = []
            for entity in self._entity_list:
                if entity.hitbox.collidepoint(self._world.camera.get_screen_position(position)):
                    if ignore_player and entity.entity_id == "player":
                        continue
                    list_of_entities.append(entity)
            return list_of_entities

    def add_entity(self, entity):
        if entity not in self._entity_list:
            self._entity_list.append(entity)

    def remove_entity(self, entity):
        if entity in self._entity_list:
            self._entity_list.remove(entity)

    def enable_flag_for_redraw(self):
        self._flag_for_redraw = True

    # Region Load and Save methods
    def convert_data(self):
        data = {"terrain": {str(x): [None for _ in range(20)] for x in range(20)}, "entity_list": []}
        for row_index, row in enumerate(self._data):
            for block_index, block in enumerate(row):
                if self._data[row_index][block_index] is not None:
                    data["terrain"][str(row_index)][block_index] = self._data[row_index][block_index].convert_data()
                else:
                    data["terrain"][str(row_index)][block_index] = None

        for entity in self._entity_list:
            data["entity_list"].append(entity.convert_data())

        return data

    def load_from_data(self, data):
        for row_index, row in data["terrain"].items():
            for block_index, block in enumerate(row):
                if block is not None:
                    self._data[int(row_index)][block_index] =\
                        self._game.block_factory.create_block(self._game, self._world,
                                                              (self._position[0] + block_index * 40,
                                                               self._position[1] + int(row_index) * 40),
                                                              block["block_id"],
                                                              block["state_data"])
                else:
                    self._data[int(row_index)][block_index] = None

        for entity in data["entity_list"]:
            entity_instance = self._game.character_factory.create_character(self._game, self._world,
                                                                            entity["entity_id"], entity["state_data"])
            self.add_entity(entity_instance)
            # if self._world.player is None and entity["entity_id"] == "player":
            # self._world.player = entity_instance
