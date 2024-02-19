import json
import os


# ADDED TO UPLOAD

class FileSaveHandler:
    def __init__(self):
        self._locations = {}

    def add_save_location(self, save_location_id, path):
        if path not in self._locations.values():
            self._locations[save_location_id] = path
            # print("added")

    def load_world(self, world, save_location_id):
        with open(self._locations[save_location_id], 'r') as f:
            if os.stat(self._locations[
                           save_location_id]).st_size > 0:
                world.load_from_data(json.load(f))
            else:
                print(
                    "SAVE FILE EMPTY. MAKING NEW WORLD INSTEAD")

    def save_world(self, world, save_location_id):
        with open(self._locations[save_location_id], "w") as f:
            json.dump(world.convert_data(), f)
