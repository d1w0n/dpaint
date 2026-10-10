import pygame

class Paint:
    def __init__(self, window, x_init, y_init, x, y, size, color):
        self._window = window
        self.x_init = x_init
        self.y_init = y_init
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def render(self, x_offset, y_offset, camera_width, camera_height, camera_zoom, debug = False):
        x_init_final = round((self.x_init + x_offset) * camera_zoom + camera_width / 2)
        y_init_final = round((self.y_init + y_offset) * camera_zoom + camera_height / 2)
        x_final = round((self.x + x_offset) * camera_zoom + camera_width / 2)
        y_final = round((self.y + y_offset) * camera_zoom + camera_height / 2)
        end_size_final = round(((self.size / 2) - 1) * camera_zoom) if round(((self.size / 2) - 1) * camera_zoom) >= 1 else 1
        line_width_final = max(round(self.size * camera_zoom), 2)

        margin = max(end_size_final, line_width_final / 2)
        left   = min(x_init_final, x_final) - margin
        right  = max(x_init_final, x_final) + margin
        top    = min(y_init_final, y_final) - margin
        bottom = max(y_init_final, y_final) + margin

        if right > 0 and left < camera_width and bottom > 0 and top < camera_height:
            pygame.draw.circle(self._window, self.color, (x_init_final, y_init_final), end_size_final)
            pygame.draw.line(self._window, self.color, (x_init_final, y_init_final), (x_final, y_final), line_width_final)
            pygame.draw.circle(self._window, self.color, (x_final, y_final), end_size_final)
            if debug: pygame.draw.rect(self._window, (255, 0, 0), (left, top, right - left, bottom - top), 1)