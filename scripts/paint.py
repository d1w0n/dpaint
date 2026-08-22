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

    def render(self, zoom, y_offset):
        pygame.draw.circle(self._window, self.color, \
            (
                round(self.x_init * zoom + (1280 / 2) * (1 - zoom)), \
                round((self.y_init + y_offset) * zoom + (960 / 2) * (1 - zoom))
            ), \
            round(((self.size / 2) - 1) * zoom)
        )

        pygame.draw.line(self._window, self.color, \
            (
                round(self.x_init * zoom + (1280 / 2) * (1 - zoom)), \
                round((self.y_init + y_offset) * zoom + (960 / 2) * (1 - zoom))
            ), \
            (
                round(self.x * zoom + (1280 / 2) * (1 - zoom)), \
                round((self.y + y_offset) * zoom + (960 / 2) * (1 - zoom))
            ), \
            round(self.size * zoom)
        )
        
        pygame.draw.circle(self._window, self.color, \
            (
                round(self.x * zoom) + ((1280 / 2) * (1 - zoom)), \
                round((self.y + y_offset) * zoom + (960 / 2) * (1 - zoom))
            ), \
            round(((self.size / 2) - 1) * zoom)
        )
    # TODO fix magic numbers (after camera class)