
class Camera:
    def __init__(self, world):
        self._world = world
        
        self._position = [0, 0]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if (type(value) is list or type(value) is tuple) and len(value) == 3:
            self._position = value

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

    def get_screen_position(self, world_position):
        return (world_position[0] - self._position[0], world_position[1] + self._position[1])



