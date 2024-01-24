
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

    def create_region_from_data(self, game, world, position, data): # Data must be converted from json string
        region = self.create_empty_region(game, world, position)
        region.load_from_data(data)
        return region

    def create_region_from_serialized(self, game, world, position, data):
        return self.create_region_from_data(game, world, position, json.loads(data))

    def create_generated_region(self, game, world, position):
        region = self.create_empty_region(game, world, position)
        self.generate_region_terrain(region)
        return region

    def randomise_seed(self):
        opensimplex.random_seed()

    def generate_region_terrain(self, region):
        for x in range(20):
            rock_y_limit_at_x = self._rock_base_level + math.trunc(opensimplex.noise2((region.position[0]+x*40)/800, 0) * 800 / 40) * 40
            grass_y_limit_at_x = self._grass_base_level + math.trunc(opensimplex.noise2((region.position[0]+x*40)/800, 1) * 400 / 40) * 40
            #print(rock_y_limit_at_x, grass_y_limit_at_x)
            for y in range(20):
                #print(region.position[1] + y*40, grass_y_limit_at_x)
                if region.position[1] + y*40 == grass_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "grass")
                elif grass_y_limit_at_x < region.position[1] + y*40 < rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "dirt")
                elif region.position[1] + y*40 >= rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "stone")

        if region.get_quantity_of_blocks_in_region("stone") > 0:
            random_stone_block = region.get_random_block_of_type_by_id("stone")
            if random_stone_block is not None:
                ores_that_can_be_generated = []
                for ore_id, ore_data in self._generation_data["ore_data"].items():
                    if ore_data["max_height"] <= random_stone_block.position[1]:
                        ores_that_can_be_generated.append((ore_id, ore_data))
                ore_to_generate = random.choice(ores_that_can_be_generated)
                region_indexes = region.get_block_indexes_from_position(random_stone_block.position)
                if random.randint(1, ore_to_generate[1]["probability"]) == 1:
                    self.generate_vein(region, ore_to_generate[0], region_indexes, ore_to_generate[1]["max_vein_size"])
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





