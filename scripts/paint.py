import pygame

class Paint:
    def __init__(self, window, x_init, y_init, x, y, size, color):
        self._window = window
        self.x_init = x_init
        self.y_init = y_init if y_init >= 0 else 0
        self.x = x
        self.y = y if y >= 0 else 0
        self.size = size
        self.color = color

    def render(self, x_offset, y_offset, camera_width, camera_height, camera_zoom):
        pygame.draw.circle(self._window, self.color, \
            (
                round((self.x_init + x_offset) * camera_zoom + (camera_width / 2) * (1 - camera_zoom)), \
                round((self.y_init + y_offset) * camera_zoom + (camera_height / 2) * (1 - camera_zoom))
            ), \
            round(((self.size / 2) - 1) * camera_zoom)
        )

        pygame.draw.line(self._window, self.color, \
            (
                round((self.x_init + x_offset) * camera_zoom + (camera_width / 2) * (1 - camera_zoom)), \
                round((self.y_init + y_offset) * camera_zoom + (camera_height / 2) * (1 - camera_zoom))
            ), \
            (
                round((self.x + x_offset) * camera_zoom + (camera_width / 2) * (1 - camera_zoom)), \
                round((self.y + y_offset) * camera_zoom + (camera_height / 2) * (1 - camera_zoom))
            ), \
            round(self.size * camera_zoom)
        )
        
        pygame.draw.circle(self._window, self.color, \
            (
                round((self.x + x_offset) * camera_zoom) + ((camera_width / 2) * (1 - camera_zoom)), \
                round((self.y + y_offset) * camera_zoom + (camera_height / 2) * (1 - camera_zoom))
            ), \
            round(((self.size / 2) - 1) * camera_zoom)
        )