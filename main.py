import pygame
import csv
import os
from scripts.paint import Paint
from scripts.ui import Text, Bar
from scripts.camera import Camera

pygame.init()

width, height = 1280, 960
window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
running = True
pen_size = 10
key_z = False
key_x = False
# TODO create camera class for camera x and y with zoom

paint = []
ui = [
    Bar(window, 0, 0, width, 25, "MenuBar", (200, 200, 200)),
    Text(window, 0, 0, "PenText", "Pen Size: " + str(pen_size) + " (Q-/W+)", 32, (0, 0, 0))
    ]
camera = Camera(window, 0, 0, width, height, 0.5)

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

    if pygame.key.get_pressed()[pygame.K_c] and not len(paint) == 0:
        paint.pop(len(paint) - 1)

    if pygame.key.get_pressed()[pygame.K_z] and not pen_size <= 1:
        if not key_z:
            key_z = True
            pen_size -= 1
            for element in ui:
                if element.name == "PenText":
                    element.set_text("Pen Size: " + str(pen_size) + " (Q-/W+)")

    else:
        key_z = False

    if pygame.key.get_pressed()[pygame.K_x]:
        if not key_x:
            key_x = True
            pen_size += 1
            for element in ui:
                if element.name == "PenText":
                    element.set_text("Pen Size: " + str(pen_size) + " (Q-/W+)")

    else:
        key_x = False

    if pygame.key.get_pressed()[pygame.K_w]:
        camera.y -= 5
    if pygame.key.get_pressed()[pygame.K_a]:
        camera.x -= 5
    if pygame.key.get_pressed()[pygame.K_s]:
        camera.y += 5
    if pygame.key.get_pressed()[pygame.K_d]:
        camera.x += 5
    if pygame.key.get_pressed()[pygame.K_q]:
        camera.zoom -= 0.05
    if pygame.key.get_pressed()[pygame.K_e]:
        camera.zoom += 0.05

    pressed = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for element in ui:
        if element.name == "MenuBar":
            mouse_y -= element.height

    if pressed:
        if was_pressed:
            paint.append(Paint(
                window, \
                old_mouse_x + camera.x, \
                old_mouse_y + camera.y, \
                mouse_x + camera.x, \
                mouse_y + camera.y, \
                pen_size, (0, 0, 0)
                ))

        else:
            paint.append(Paint(window, mouse_x + camera.x, mouse_y + camera.y, mouse_x + camera.x, mouse_y + camera.y, pen_size, (0, 0, 0)))

    was_pressed = pressed
    old_mouse_x, old_mouse_y = mouse_x, mouse_y

    for element in ui:
        if element.name == "MenuBar":
            for line in paint:
                line.render(-camera.x, element.height - camera.y, camera.width, camera.height, camera.zoom)
    
    for element in ui:
        element.render()

    pygame.display.flip()
    clock.tick(60)

save_data = [
    ["x_init", "y_init", "x", "y", "size", "red", "green", "blue"]
]

for line in paint:
    save_data.append([line.x_init, line.y_init, line.x, line.y, line.size, line.color[0], line.color[1], line.color[2]])

with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(save_data)

pygame.quit()