from src.world.Region import Region
import json

class RegionGenerator:
    def __init__(self):
        pass

    def create_empty_region(self, game, world, position):
        return Region(game, world, position)

    def create_region_from_data(self, game, world, position, data): # Data must be converted from json string
        region = self.create_empty_region(game, world, position)
        region.load_from_data(data)
        return region

    def create_region_from_serialized(self, game, world, position, data):
        return self.create_region_from_data(game, world, position, json.loads(data))

    def create_generated_region(self, game, world, position):
        pass

    def generate_region_terrain(self, region):
        pass