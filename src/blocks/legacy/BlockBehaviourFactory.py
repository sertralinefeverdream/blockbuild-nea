from src.blocks.legacy.BasicBehaviour import BasicBehaviour


class BlockBehaviourFactory:
    def __init__(self, audio_handler_factory):
        self._audio_handler_factory = audio_handler_factory

    def create_block_behaviour(self, game, block_behaviour_id, *args):
        if block_behaviour_id.lower() == "basic":
            return BasicBehaviour(self._audio_handler_factory.create_handler("sfxhandler", game), *args)
        else:
            raise NotImplementedError
