
from src.world.Region import Region
import json
import math
import opensimplex

class RegionGenerator:
    def __init__(self):
        opensimplex.random_seed()

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

    def generate_region_terrain(self, region):
        for x in range(20):
            rock_y_limit_at_x = math.trunc(1600 + opensimplex.noise2(region.position[0] + x, 0) * 400)
            grass_y_limit_at_x = math.trunc(800 + opensimplex.noise2(region.position[0] + x, 0) * 400)
            for y in range(20):
                if region.position[1] + y*40 == grass_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "grass")
                if region.position[1] + y*40 == rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "stone")
