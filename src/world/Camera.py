
class Camera:
    def __init__(self):
        self._position = [0, 0]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 3:
            self._position = list(value)

    @property
    def min_x(self):
        return self._position[0]

    def max_x(self):
        return self._position[1]

    @property
    def min_y(self):
        return self._position[1]

    @property
    def max_y(self):
        return self._position[1] + 800

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, value):
        if type(value) is float or type(value) is int:
            self._position[0] = value

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, value):
        if type(value) is float or type(value) is int:
            self._position[1] = value

    def get_screen_position(self, position):
        if (type(position) is list or type(position) is tuple) and len(position) == 2:
            offset_x = -self._position[0]
            offset_y = -self._position[1]

            return position[0] + offset_x, position[1] + offset_y






