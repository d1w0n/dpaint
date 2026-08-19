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

class Paint:
    def __init__(self, window, x_init, y_init, x, y, radius, color):
        self._window = window
        self.x_init = x_init
        self.y_init = y_init
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def render(self):
        pygame.draw.circle(self._window, self.color, (self.x_init, self.y_init), self.radius - 1)
        pygame.draw.line(self._window, self.color, (self.x_init, self.y_init), (self.x, self.y), self.radius * 2)
        pygame.draw.circle(self._window, self.color, (self.x, self.y), self.radius - 1)

pygame.init()

width, height = 1280, 960
window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
running = True

pen_radius = 5
key_q = False
key_w = False

instances = []
ui = [Text(window, 0, 0, "PenText", "Pen Size: " + str(pen_radius) + " (Q-/W+)", 32, (0, 0, 0))]

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.csv")
    
if os.path.exists(save_path):
    try:
        with open(save_path, "r") as save:
            csv_reader = csv.DictReader(save)
            for row in csv_reader:
                instances.append(Paint(window, \
                    int(row["x_init"]), \
                    int(row["y_init"]), \
                    int(row["x"]), \
                    int(row["y"]), \
                    int(row["radius"]), \
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

    if pygame.key.get_pressed()[pygame.K_z] and not len(instances) == 0:
        instances.pop(len(instances) - 1)

    if pygame.key.get_pressed()[pygame.K_q] and not pen_radius <= 1:
        if not key_q:
            key_q = True
            pen_radius -= 1
            for element in ui:
                if element.name == "PenText":
                    element.set_text("Pen Size: " + str(pen_radius) + " (Q-/W+)")

    else:
        key_q = False

    if pygame.key.get_pressed()[pygame.K_w]:
        if not key_w:
            key_w = True
            pen_radius += 1
            for element in ui:
                if element.name == "PenText":
                    element.set_text("Pen Size: " + str(pen_radius) + " (Q-/W+)")

    else:
        key_w = False

    pressed = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if pressed:
        if was_pressed:
            instances.append(Paint(window, old_mouse_x, old_mouse_y, mouse_x, mouse_y, pen_radius, (0, 0, 0)))

        else:
            instances.append(Paint(window, mouse_x, mouse_y, mouse_x, mouse_y, pen_radius, (0, 0, 0)))

    was_pressed = pressed
    old_mouse_x, old_mouse_y = mouse_x, mouse_y

    for instance in instances:
        instance.render()

    for element in ui:
        element.render()

    pygame.display.flip()
    clock.tick(60)

save_data = [
    ["x_init", "y_init", "x", "y", "radius", "red", "green", "blue"]
]

for instance in instances:
    save_data.append([instance.x_init, instance.y_init, instance.x, instance.y, instance.radius, instance.color[0], instance.color[1], instance.color[2]])
# adds player data to the save.

with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(save_data)

pygame.quit()
