from src.gui.TextButton import TextButton
from src.gui.TextLabel import TextLabel
from src.gui.RectBox import RectBox
from src.gui.HotbarDisplay import HotbarDisplay
from src.gui.ItemDisplay import ItemDisplay
from src.gui.ContainerDisplayInteractive import ContainerDisplayInteractive
from src.gui.ItemButton import ItemButton

'''
This GUIFactory class has allowed me to remove any dependence of StateBase and its child classes on any of the
GUI classes. GUIFactory instance is passed as an argument during StateBase initialisation.
'''

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
        else:
            raise Exception

