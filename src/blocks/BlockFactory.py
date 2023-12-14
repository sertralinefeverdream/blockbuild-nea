from src.blocks.Block import Block


class BlockFactory:
    def __init__(self, block_dict, block_behaviour_factory):
        self._block_dict = block_dict
        self._block_behaviour_factory = block_behaviour_factory

    def create_block(self, game, block_id):
        if block_id in self._block_dict.keys():
            block_data = self._block_dict[block_id]
            block_behaviour = self._block_behaviour_factory.create_block_behaviour(game, block_data["behaviour"])
            block = Block(game, block_behaviour, block_data["texture"])
            block_behaviour.block = block
            return block

