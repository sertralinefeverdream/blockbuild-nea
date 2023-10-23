from src.gui.TextButton import TextButton
from src.gui.TextLabel import TextLabel

class GUIFactory:
    def __init__(self):
        pass

    def create_component(self, component_id, *args, **kwargs):
        if component_id == "TextButton":
            print("made textbutton")
            return TextButton(*args, **kwargs)
        elif component_id == "TextLabel":
            return TextLabel(*args, **kwargs)
        else:
            return None
