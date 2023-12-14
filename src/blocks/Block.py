class Block:
    def __init__(self, block_behaviour_factory, block_data_factory):
        self._block_behaviour = None
        self._block_behaviour_factory = block_behaviour_factory
        self._block_data_factory = block_data_factory
        self._block_data = None

    def set_block_behaviour(self, behaviour_id):


    def set_block_data(self, data_id):
        pass

    def update(self):
        if self._block_behaviour is not None and self._block_data is not None:
            self._block_behaviour.update()
        else:
            raise NotImplementedError

    def draw(self):
        if self._block_behaviour is not None and self._block_data is not None:
            pass
        else:
            raise NotImplementedError
