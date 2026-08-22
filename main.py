import pygame
import csv
import os

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

pygame.init()

width, height = 1280, 960
window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
running = True
pen_size = 10
key_q = False
key_w = False
zoom = 0.9
# TODO create camera class for camera x and y with zoom

paint = []
ui = [
    Bar(window, 0, 0, width, 25, "MenuBar", (200, 200, 200)),
    Text(window, 0, 0, "PenText", "Pen Size: " + str(pen_size) + " (Q-/W+)", 32, (0, 0, 0))
    ]

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.csv")
    
if os.path.exists(save_path):
    try:
        with open(save_path, "r") as save:
            csv_reader = csv.DictReader(save)
            for row in csv_reader:
                paint.append(Paint(window, \
                    int(row["x_init"]), \
                    int(row["y_init"]), \
                    int(row["x"]), \
                    int(row["y"]), \
                    int(row["size"]), \
                    (int(row["red"]), int(row["green"]), int(row["blue"]))
                    ))
    except:
        pass
else:
    open(save_path, mode="w", newline="")

old_mouse_x, old_mouse_y = pygame.mouse.get_pos()
was_pressed = False

while running:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    if pygame.key.get_pressed()[pygame.K_z] and not len(paint) == 0:
        paint.pop(len(paint) - 1)

    if pygame.key.get_pressed()[pygame.K_q] and not pen_size <= 1:
        if not key_q:
            key_q = True
            pen_size -= 1
            for element in ui:
                if element.name == "PenText":
                    element.set_text("Pen Size: " + str(pen_size) + " (Q-/W+)")

    else:
        key_q = False

    if pygame.key.get_pressed()[pygame.K_w]:
        if not key_w:
            key_w = True
            pen_size += 1
            for element in ui:
                if element.name == "PenText":
                    element.set_text("Pen Size: " + str(pen_size) + " (Q-/W+)")

    else:
        key_w = False

    pressed = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for element in ui:
        if element.name == "MenuBar":
            mouse_y -= element.height

    if pressed:
        if was_pressed:
            paint.append(Paint(window, old_mouse_x, old_mouse_y, mouse_x, mouse_y, pen_size, (0, 0, 0)))

        else:
            paint.append(Paint(window, mouse_x, mouse_y, mouse_x, mouse_y, pen_size, (0, 0, 0)))

    was_pressed = pressed
    old_mouse_x, old_mouse_y = mouse_x, mouse_y

    for element in ui:
        if element.name == "MenuBar":
            for stroke in paint:
                stroke.render(zoom, element.height)
    
    for element in ui:
        element.render()

    pygame.display.flip()
    clock.tick(60)

save_data = [
    ["x_init", "y_init", "x", "y", "size", "red", "green", "blue"]
]

for stroke in paint:
    save_data.append([stroke.x_init, stroke.y_init, stroke.x, stroke.y, stroke.size, stroke.color[0], stroke.color[1], stroke.color[2]])

with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(save_data)

pygame.quit()