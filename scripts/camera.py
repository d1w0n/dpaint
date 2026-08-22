class Camera:
    def __init__(self, window, x, y, width, height, zoom):
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoom = zoom