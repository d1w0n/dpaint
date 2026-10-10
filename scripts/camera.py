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
        self.ZOOM_PRESETS = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.5, 10.0]
        self._zoom_preset = 3

    @property
    def zoom_preset(self): return self._zoom_preset

    @zoom_preset.setter
    def zoom_preset(self, x: int):
        if x >= 0 and x < len(self.ZOOM_PRESETS): self._zoom_preset = x
        self.zoom = self.ZOOM_PRESETS[self._zoom_preset]

    def set_old(self):
        self.old_x = self.x
        self.old_y = self.y
        self.old_zoom = self.zoom