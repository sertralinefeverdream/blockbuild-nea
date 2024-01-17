import json

class FileSaveHandler:
    def __init__(self):
        self._locations = {}

    def add_save_location(self, save_location_id, path):
        if path not in self._locations.values():
            self._locations[save_location_id] = path
            print("added")

    def load_world(self, world, save_location_id):
        with open(self._locations[save_location_id], 'r') as f:
            world.load_from_data(json.load(f))

    def save_world(self, world, save_location_id):
        with open(self._locations[save_location_id], "w") as f:
            json.dump(world.convert_data(), f)

