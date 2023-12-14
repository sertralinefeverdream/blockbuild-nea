from src.blocks.BlockBehaviour import BlockBehaviour

class BasicBehaviour(BlockBehaviour):
    def __init__(self, audio_handler):
        super().__init__(audio_handler)

    def update(self):
        print("Hello world!")