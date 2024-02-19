from gui.GUIBase import GUIBase

#uploaded

class ContainerDisplayInteractive(GUIBase):
    def __init__(self, game, surface, rows, columns, click_func, hover_enter_func=None, hover_leave_func=None,
                 held_func=None, position=(0.0, 0.0), is_visible=True, ):
        super().__init__(game, surface, position, is_visible)
        self._container = None
        self._dimensions = (rows, columns)  # y, x orientation
        self._gui = [[self._game.gui_factory.create_gui("ItemButton", game, surface, click_func,
                                                        hover_enter_func=hover_enter_func,
                                                        hover_leave_func=hover_leave_func, held_func=held_func,
                                                        size=(60.0, 60.0)) for x in range(self._dimensions[1])] for y in
                     range(self._dimensions[0])]

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def gui(self):
        return self._gui

    @property
    def centre_position(self):
        return self._position[0] + (self._dimensions[1] * 60) / 2, self._position[1] + (self._dimensions[0] * 60) / 2

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._position = value[0] - (self._dimensions[1] * 60) / 2, value[1] - (self._dimensions[0] * 60) / 2

    def update(self):
        if self._container is not None:
            for row_index, row in enumerate(self._container.data):
                for item_index, item in enumerate(row):
                    self._gui[row_index][item_index].item = item
                    self._gui[row_index][item_index].position = (
                    self._position[0] + item_index * 60, self._position[1] + row_index * 60)
                    self._gui[row_index][item_index].update()

    def draw(self):
        for row in self._gui:
            for item in row:
                item.draw()

    def get_hovering(self):
        for row in self._gui:
            for item_slot in row:
                if item_slot.is_hovering:
                    return item_slot
        return None
