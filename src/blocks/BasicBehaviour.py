from src.blocks.BlockBehaviour import BlockBehaviour


class BasicBehaviour(BlockBehaviour):
    def __init__(self, audio_handler):
        super().__init__(audio_handler)

    def update(self):
        if self._block is not None:
            print("Hello world!")
        else:
            raise NotImplementedError
