from world.Region import Region
import json
import math
import opensimplex
import random

#uploaded


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
        # print(f"SEED SAVED: {opensimplex.get_seed()} ")
        return opensimplex.get_seed()

    @seed.setter
    def seed(self, value):
        if type(value) is int:
            # print(f"SET SEED: {value}")
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
        self.generate_region_terrain(region)
        self.populate_region_with_ores(region)
        return region

    def randomise_seed(self):
        opensimplex.random_seed()

    def generate_region_terrain(self, region):
        has_generated_tree_in_region = False
        for x in range(20):
            rock_y_limit_at_x = self._rock_base_level + math.trunc(
                opensimplex.noise2((region.position[0] + x * 40) / 800, 0) * 800 / 40) * 40
            grass_y_limit_at_x = self._grass_base_level + math.trunc(
                opensimplex.noise2((region.position[0] + x * 40) / 800, 1) * 400 / 40) * 40
            for y in range(20):
                if region.position[1] + y * 40 == grass_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "grass")
                    if has_generated_tree_in_region == False:
                        if random.randint(1, 5) == 1:
                            tree_to_generate = random.choice(list(self._generation_data["tree_data"].values()))
                            generated_successfully = self.generate_tree_in_region(region,
                                                                                  tree_to_generate["trunk_block_id"],
                                                                                  tree_to_generate["leaf_block_id"],
                                                                                  (x, y - 1),
                                                                                  tree_to_generate["trunk_length"],
                                                                                  tree_to_generate[
                                                                                      "leaf_base_layer_width"])
                            if generated_successfully:
                                has_generated_tree_in_region = True
                elif grass_y_limit_at_x < region.position[1] + y * 40 < rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "dirt")
                elif region.position[1] + y * 40 >= rock_y_limit_at_x:
                    region.set_block_at_indexes(x, y, "stone")

    def generate_tree_in_region(self, region, trunk_block_id, leaf_block_id, starting_indexes, trunk_length,
                                leaf_base_layer_width):
        trunk_block_indexes = []
        leaf_block_indexes = []

        current_indexes = list(starting_indexes[::1])

        for x in range(random.randint(3, trunk_length)):
            if 0 <= current_indexes[0] <= 19 and 0 <= current_indexes[1] <= 19:
                if region.get_block_at_indexes(*current_indexes) is None:
                    trunk_block_indexes.append(tuple(current_indexes))
                else:
                    # print("TRUNK OBSTRUCTED")
                    return False
            else:
                # print("TRUNK FALLEN OFF REGION")
                return False
            current_indexes[1] -= 1
        # SCREEN SHOT MARKER
        for i in range(leaf_base_layer_width):
            if 0 <= current_indexes[1] <= 19:
                if region.get_block_at_indexes(*current_indexes) is None:
                    leaf_block_indexes.append(tuple(current_indexes))
                    for j in range(leaf_base_layer_width - i):
                        if j == 0: continue
                        if 0 <= current_indexes[0] + j <= 19 and 0 <= current_indexes[0] - j <= 19:
                            if region.get_block_at_indexes(
                                    current_indexes[0] + j, current_indexes[1]) is None and region.get_block_at_indexes(
                                current_indexes[0] - j, current_indexes[1]) is None:
                                leaf_block_indexes.append((current_indexes[0] + j, current_indexes[1]))
                                leaf_block_indexes.append((current_indexes[0] - j, current_indexes[1]))
                            else:
                                # print("CANT SPAWN HERE DUE TO LEAF OBSTRUCTION") SCREENSHOT MARKER

                                return False  ## Screenshot Marker
                        else:
                            # print("FALLEN OFF")
                            return False
                    current_indexes[1] -= 1
                else:
                    return False
            else:
                return False

        for x, y in leaf_block_indexes:
            region.set_block_at_indexes(x, y, leaf_block_id)

        for x, y in trunk_block_indexes:
            region.set_block_at_indexes(x, y, trunk_block_id)

        return True

    def populate_region_with_ores(self, region):
        if region.get_quantity_of_blocks_in_region("stone") > 0:
            random_stone_block = region.get_random_block_of_type_by_id("stone")
            if random_stone_block is not None:
                ores_that_can_be_generated = []
                for ore_id, ore_data in self._generation_data["ore_data"].items():
                    if random_stone_block.position[1] >= ore_data["max_height"]:
                        ores_that_can_be_generated.append(ore_data)
                if len(ores_that_can_be_generated) == 0: return None
                ore_to_generate = random.choice(ores_that_can_be_generated)
                region_indexes = region.get_block_indexes_from_position(random_stone_block.position)
                if random.randint(1, ore_to_generate["probability"]) == 1:
                    # print("GENERATING ORE!!")
                    self.generate_vein(region, ore_to_generate["block_id"], region_indexes,
                                       ore_to_generate["max_vein_size"])

    def generate_vein(self, region, block_id, starting_indexes, max_vein_size):
        x, y = starting_indexes
        ores_generated = 0
        amount_to_generate = random.randint(1, max_vein_size)
        while ores_generated < amount_to_generate:
            x += random.choice([-1, 0, 1])
            y += random.choice([-1, 0, 1])
            x = 19 if x > 19 else 0 if x < 0 else x
            y = 19 if y > 19 else 0 if y < 0 else y

            block_at_indexes = region.get_block_at_indexes(x, y)
            if block_at_indexes is not None:
                if block_at_indexes.block_id == block_id:
                    continue
            region.set_block_at_indexes(x, y, block_id)
            ores_generated += 1
