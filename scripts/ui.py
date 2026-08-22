import pygame

class Text:
    def __init__(self, window, x, y, name, text, size, color):
        self._window = window 
        self.x = x
        self.y = y
        self.name = name
        self.size = size
        self.color = color
        self.font = pygame.font.Font(None, size)
        self._text_surface = self.font.render(text, True, self.color)

    def render(self):
        self._window.blit(self._text_surface, (self.x, self.y))

    def set_text(self, text: str):
        self._text_surface = self.font.render(text, True, self.color)

class Bar:
    def __init__(self, window, x, y, width, height, name, color):
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self):
        pygame.draw.rect(self._window, self.color, self.rect)