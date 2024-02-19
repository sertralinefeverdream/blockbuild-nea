from audio.MusicHandler import MusicHandler
from audio.SfxHandler import SfxHandler

#UPLOADED

class AudioHandlerFactory:
    def __init__(self):
        pass

    def create_handler(self, component_id, *args, **kwargs):
        if component_id.lower() == "musichandler":
            return MusicHandler(*args, **kwargs)
        elif component_id.lower() == "sfxhandler":
            return SfxHandler(*args, **kwargs)
