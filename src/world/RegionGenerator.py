
from src.world.Region import Region
import json
import math
import opensimplex

class RegionGenerator:
    def __init__(self, rock_base_level=1200, grass_base_level=400):
        opensimplex.random_seed()
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


