from src.audio.MusicHandler import MusicHandler
from src.audio.SfxHandler import SfxHandler

class AudioHandlerFactory:
    def __init__(self):
        pass

    def create_handler(self, component_id, *args, **kwargs):
        if component_id == "MusicHandler":
            return MusicHandler(*args, **kwargs)
        elif component_id == "SfxHandler":
            return SfxHandler(*args, **kwargs)