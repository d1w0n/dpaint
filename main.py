import pygame
import csv
import os
from scripts.paint import Paint
from scripts.ui import Text, Bar
from scripts.camera import Camera

def create_menu_text(camera_zoom, camera_x, camera_y, pen_size, pen_color):
    return "Zoom Level: " + str(round(camera_zoom * 100)) + "% (Q-/W+), " \
            "Coordinates: (" + str(camera_x) + ", " + str(camera_y) + ") (WASD), " \
            "Pen Size: " + str(pen_size) + " (Z-/X+), " \
            "Pen Color: " + str(pen_color) + " (1/2/3)"

pygame.init()

width, height = 1280, 960
window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
running = True
pen_size = 10
pen_color = (0, 0, 0)
key_z = False
key_x = False
key_c = False
# initialize program variables.

paint = []
camera = Camera(window, 0, 0, width, height, 1.0)
ui = [
    Bar(window, 0, 0, width, 25, "MenuBar", (200, 200, 200)),
    Text(window, 5, 0, "MenuText", create_menu_text(camera.zoom, camera.x, camera.y, pen_size, pen_color), 32, (0, 0, 0))
    ]
# initialize program gui.

for element in ui:
    if element.name == "MenuBar":
        ui.append(Bar(window, element.width - element.height, 0, element.height, element.height, "ColorBar", (0, 0, 0)))
# pen color indicator.

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.csv")
    
if os.path.exists(save_path):
    try:
        with open(save_path, "r") as save:
            csv_reader = csv.DictReader(save)
            for row in csv_reader:
                paint.append(Paint(window, int(row["x_init"]), int(row["y_init"]), int(row["x"]), int(row["y"]), int(row["size"]), (int(row["red"]), int(row["green"]), int(row["blue"]))))
                
    except:
        pass

else:
    pass
# loads save.csv.

old_mouse_x, old_mouse_y = pygame.mouse.get_pos()
old_camera_zoom = camera.zoom
old_camera_x, old_camera_y = camera.x, camera.y
was_pressed = False

while running:
    key = pygame.key.get_pressed()

    if key[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    if key[pygame.K_c] and not len(paint) == 0:
        paint.pop(len(paint) - 1)

    if key[pygame.K_z] and not pen_size <= 1:
        if not key_z:
            key_z = True
            pen_size -= 1

    else:
        key_z = False

    if key[pygame.K_x]:
        if not key_x:
            key_x = True
            pen_size += 1

    else:
        key_x = False

    if key[pygame.K_1] and not key[pygame.K_LALT] and not pen_color[0] == 255:
        pen_color = (pen_color[0] + 1, pen_color[1], pen_color[2])

    if key[pygame.K_2] and not key[pygame.K_LALT] and not pen_color[1] == 255:
        pen_color = (pen_color[0], pen_color[1] + 1, pen_color[2])

    if key[pygame.K_3] and not key[pygame.K_LALT] and not pen_color[2] == 255:
        pen_color = (pen_color[0], pen_color[1], pen_color[2] + 1)

    if key[pygame.K_1] and key[pygame.K_LALT] and not pen_color[0] == 0:
        pen_color = (pen_color[0] - 1, pen_color[1], pen_color[2])

    if key[pygame.K_2] and key[pygame.K_LALT] and not pen_color[1] == 0:
        pen_color = (pen_color[0], pen_color[1] - 1, pen_color[2])

    if key[pygame.K_3] and key[pygame.K_LALT] and not pen_color[2] == 0:
        pen_color = (pen_color[0], pen_color[1], pen_color[2] - 1)

    if key[pygame.K_w]:
        camera.y -= round(5 / camera.zoom)
    if key[pygame.K_a]:
        camera.x -= round(5 / camera.zoom)
    if key[pygame.K_s]:
        camera.y += round(5 / camera.zoom)
    if key[pygame.K_d]:
        camera.x += round(5 / camera.zoom)
    if key[pygame.K_q]:
        camera.zoom -= 0.05
    if key[pygame.K_e]:
        camera.zoom += 0.05

    if any(key):
        for element in ui:
            if element.name == "MenuText":
                element.set_text(create_menu_text(camera.zoom, camera.x, camera.y, pen_size, pen_color))

            elif element.name == "ColorBar":
                element.color = pen_color

    pressed = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for element in ui:
        if element.name == "MenuBar":
            mouse_y -= element.height

    if pressed:
        if was_pressed:
            paint.append(Paint(
                window,
                round((old_mouse_x - camera.width / 2) / old_camera_zoom + old_camera_x),
                round((old_mouse_y - camera.height / 2) / old_camera_zoom + old_camera_y),
                round((mouse_x - camera.width / 2) / camera.zoom + camera.x),
                round((mouse_y - camera.height / 2) / camera.zoom + camera.y),
                pen_size, pen_color
                ))

        else:
            paint.append(Paint(
                window,
                round((mouse_x - camera.width / 2) / camera.zoom + camera.x),
                round((mouse_y - camera.height / 2) / camera.zoom + camera.y),
                round((mouse_x - camera.width / 2) / camera.zoom + camera.x),
                round((mouse_y - camera.height / 2) / camera.zoom + camera.y),
                pen_size, pen_color
                ))
            
    was_pressed = pressed
    old_mouse_x, old_mouse_y = mouse_x, mouse_y
    old_camera_zoom = camera.zoom
    old_camera_x, old_camera_y = camera.x, camera.y

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