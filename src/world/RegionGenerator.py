from src.world.Region import Region
import json

class RegionGenerator:
    def __init__(self):
        pass

    def create_empty_region(self, game, position):
        return Region(game, position)

    def create_region_from_data(self, game, position, data): # Data must be converted from json string
        region = self.create_empty_region(game, position)
        region.load_from_data(data)
        return region

    def create_region_from_serialized(self, game, position, data):
        return self.create_region_from_data(game, position, json.loads(data))

    def create_generated_region(self, game, position):
        pass

    def generate_region_terrain(self, region):
        pass