from gui.TextButton import TextButton
from gui.TextLabel import TextLabel
from gui.RectBox import RectBox
from gui.HotbarDisplay import HotbarDisplay
from gui.ItemDisplay import ItemDisplay
from gui.ContainerDisplayInteractive import ContainerDisplayInteractive
from gui.ItemButton import ItemButton
from gui.ImageButton import ImageButton

#uploaded

class GUIFactory:
    def __init__(self):
        pass

    def create_gui(self, component_id, *args, **kwargs):
        if component_id == "TextButton":
            return TextButton(*args, **kwargs)
        elif component_id == "TextLabel":
            return TextLabel(*args, **kwargs)
        elif component_id == "RectBox":
            return RectBox(*args, **kwargs)
        elif component_id == "ItemDisplay":
            return ItemDisplay(*args, **kwargs)
        elif component_id == "HotbarDisplay":
            return HotbarDisplay(*args, **kwargs)
        elif component_id == "ContainerDisplayInteractive":
            return ContainerDisplayInteractive(*args, **kwargs)
        elif component_id == "ItemButton":
            return ItemButton(*args, **kwargs)
        elif component_id == "ImageButton":
            return ImageButton(*args, **kwargs)
        else:
            raise Exception
