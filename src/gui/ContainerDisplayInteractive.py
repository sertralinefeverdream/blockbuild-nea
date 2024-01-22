from src.gui.GUIBase import GUIBase

class ContainerDisplayInteractive(GUIBase):
    def __init__(self, game, surface, rows, columns, click_func, position=(0.0, 0.0), is_visible=True):
        super().__init__(game, surface, position, is_visible)
        self._container = None
        self._dimensions = (rows, columns) # y, x orientation
        self._gui = [[self._game.gui_factory.create_gui("ItemButton", game, surface, click_func, size=(60.0, 60.0)) for x in range(self._dimensions[1])] for y in range(self._dimensions[0])]

    @property
    def centre_position(self):
        return self._position[0] + (self._dimensions[1]*60)/2, self._position[1] + (self._dimensions[0]*60)/2

    @centre_position.setter
    def centre_position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 2:
            self._position = value[0] - (self._dimensions[1] * 60)/2, value[1] - (self._dimensions[0]*60)/2

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value

    @property
    def gui(self):
        return self._gui

    def update(self):
        if self._container is not None:
            for row_index, row in enumerate(self._container.data):
                for item_index, item in enumerate(row):
                    self._gui[row_index][item_index].item = item
                    self._gui[row_index][item_index].position = (self._position[0]+item_index*60, self._position[1]+row_index*60)
                    self._gui[row_index][item_index].update()

    def draw(self):
        for row in self._gui:
            for item in row:
                item.draw()


