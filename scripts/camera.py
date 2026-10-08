class Camera:
    def __init__(self, window, x, y, width, height, zoom):
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoom = zoom
        self.old_x = x
        self.old_y = y
        self.old_zoom = zoom

    def set_old(self):
        self.old_x = self.x
        self.old_y = self.y
        self.old_zoom = self.zoom