from src.world.Region import Region
import json
import math
import opensimplex
import random


class RegionGenerator:
    def __init__(self, generation_data, rock_base_level=1200, grass_base_level=400):
        opensimplex.random_seed()
        self._generation_data = generation_data
        self._rock_base_level = rock_base_level
        self._grass_base_level = grass_base_level

    @property
    def generation_data(self):
        return self._generation_data

    @property
    def seed(self):
        print(f"SEED SAVED: {opensimplex.get_seed()} ")
        return opensimplex.get_seed()

    @seed.setter
    def seed(self, value):
        if type(value) is int:
            print(f"SET SEED: {value}")
            opensimplex.seed(value)

    def create_empty_region(self, game, world, position):
        return Region(game, world, position)

    def create_region_from_data(self, game, world, position, data):  # Data must be converted from json string
        region = self.create_empty_region(game, world, position)
        region.load_from_data(data)
        return region

    def create_region_from_serialized(self, game, world, position, data):
        return self.create_region_from_data(game, world, position, json.loads(data))

    def create_generated_region(self, game, world, position):
        region = self.create_empty_region(game, world, position)
        self.generate_region_terrain(world, region)
        return region

    def randomise_seed(self):
        opensimplex.random_seed()

    def generate_region_terrain(self, world, region):
        for x in range(20):
            rock_y_limit_at_x = self._rock_base_level + math.trunc(
                opensimplex.noise2((region.position[0] + x * 40) / 800, 0) * 800 / 40) * 40
            grass_y_limit_at_x = self._grass_base_level + math.trunc(
                opensimplex.noise2((region.position[0] + x * 40) / 800, 1) * 400 / 40) * 40
            # print(rock_y_limit_at_x, grass_y_limit_at_x)
            for y in range(20):
                # print(region.position[1] + y*40, grass_y_limit_at_x)
                if region.position[1] + y * 40 == grass_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "grass")

                elif grass_y_limit_at_x < region.position[1] + y * 40 < rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "dirt")
                elif region.position[1] + y * 40 >= rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "stone")

    def generate_tree(self, world, trunk_block_id, leaf_block_id, starting_position, trunk_length,
                      leaf_base_layer_width):

        trunk_block_indexes = []
        leaf_block_indexes = []

        current_position = list(starting_position[::1])

        for x in range(trunk_length):
            if world.get_block_at_position(current_position) is None:
                print(f"CURRENT POSITION 1:", current_position)
                trunk_block_indexes.append(tuple(current_position))
                print("CURRENT POSITION 2: ", current_position)
                current_position[1] -= 40
                print(trunk_block_indexes, " TRUNK INDEXES HERE")

            else:
                print("CANT SPAWN TREE HERE DUE TO TRUNK OBSTRUCTION")
                return None

        for i in range(leaf_base_layer_width):
            if world.get_block_at_position((current_position[0], current_position[1])) is None:
                leaf_block_indexes.append((current_position[0], current_position[1]))
                for j in range(leaf_base_layer_width - i):
                    if world.get_block_at_position(
                            (current_position[0] + j*40, current_position[1])) is None and world.get_block_at_position(
                            (current_position[0] - j*40, current_position[1])) is None:
                        leaf_block_indexes.append((current_position[0] + j*40, current_position[1]))
                        leaf_block_indexes.append((current_position[0] - j*40, current_position[1]))
                    else:
                        print("CANT SPAWN HERE DUE TO LEAF OBSTRUCTION")
                        return None
                current_position[1] -= 40
            else:
                return None

        print(leaf_block_indexes)
        print(trunk_block_indexes)

        for x, y in leaf_block_indexes:
            world.set_block_at_position((x, y), leaf_block_id)

        for x, y in trunk_block_indexes:
            world.set_block_at_position((x, y), trunk_block_id)

    def populate_region_with_ores(self, region):
        if region.get_quantity_of_blocks_in_region("stone") > 0:
            random_stone_block = region.get_random_block_of_type_by_id("stone")
            if random_stone_block is not None:
                ores_that_can_be_generated = []
                for ore_id, ore_data in self._generation_data["ore_data"].items():
                    if random_stone_block.position[1] >= ore_data["max_height"]:
                        ores_that_can_be_generated.append(ore_data)
                ore_to_generate = random.choice(ores_that_can_be_generated)
                region_indexes = region.get_block_indexes_from_position(random_stone_block.position)
                if random.randint(1, ore_to_generate["probability"]) == 1:
                    self.generate_vein(region, ore_to_generate["block_id"], region_indexes,
                                       ore_to_generate["max_vein_size"])
            else:
                print("NO STONE BLOCKS HERE ")

    def generate_vein(self, region, block_id, starting_indexes, max_max_vein_size):
        x, y = starting_indexes

        ores_generated = 0
        amount_to_generate = random.randint(1, max_max_vein_size)
        while ores_generated < amount_to_generate:
            x += random.choice([-1, 0, 1])
            y += random.choice([-1, 0, 1])

            x = 19 if x > 19 else 0 if x < 0 else x
            y = 19 if y > 19 else y if y < 0 else y

            block_at_indexes = region.get_block_at_indexes(x, y)
            if block_at_indexes is not None:
                if block_at_indexes.block_id == block_id:
                    continue

            region.set_block_at_indexes(x, y, block_id)
            ores_generated += 1
