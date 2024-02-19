from gui.GUIBase import GUIBase

#uploaded

class HotbarDisplay(GUIBase):
    def __init__(self, game, surface, number_of_slots, position=(0.0, 0.0), is_visible=True,
                 current_item_colour=(255, 255, 255), default_item_colour=(170, 170, 170)):
        super().__init__(game, surface, position, is_visible)
        self._hotbar = None
        self._number_of_slots = number_of_slots  # No. of
        self._current_item_colour = current_item_colour
        self._default_item_colour = default_item_colour
        self._gui = [self._game.gui_factory.create_gui("ItemDisplay", game, surface, size=(60.0, 60.0)) for x in
                     range(self._number_of_slots)]

    @property
    def hotbar(self):
        return self._hotbar

    @hotbar.setter
    def hotbar(self, value):
        self._hotbar = value

    @property
    def centre_position(self):
        return self._position[0] + (self._number_of_slots * 60) / 2, self._position[1] + 30

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._position = value[0] - (self._number_of_slots * 60) / 2, value[1] - ((60) / 2)

    def update(self):
        if self._hotbar is not None:
            for item_index, item in enumerate(self._hotbar.data[0]):
                self._gui[item_index].item = item
                self._gui[item_index].position = (self._position[0] + item_index * 60, self._position[1])
                self._gui[item_index].update()
                if item_index == self._hotbar.current_item_pointer:
                    self._gui[item_index].box_colour = self._current_item_colour
                else:
                    self._gui[item_index].box_colour = self._default_item_colour

    def draw(self):
        for slot in self._gui:
            slot.draw()
