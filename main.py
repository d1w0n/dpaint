import pygame
import csv
import os
import math
from scripts.paint import Paint
from scripts.ui import Text, Bar
from scripts.camera import Camera
from scripts.pen import Pen

def single_key_press(input, dict, key) -> bool:
    if input: 
        if not dict[key]:
            dict[key] = True
            return True
        
        else: return False

    else: 
        dict[key] = False
        return False

def create_menu_text(alt_keys, camera_zoom, camera_x, camera_y, pen_size, pen_color) -> str:
    if not alt_keys: return "Zoom Level: " + str(round(camera_zoom * 100)) + "% (Q-/W+), " \
        "Coordinates: (" + str(round(camera_x)) + ", " + str(round(camera_y)) + ") (WASD), " \
        "Pen Size: " + str(pen_size) + " (Z-/X+), " \
        "Pen Color: " + str(pen_color) + " (1/2/3)+"
    
    else: return "Zoom Level: " + str(round(camera_zoom * 100)) + "% (Q-/W+), " \
        "Coordinates: (" + str(round(camera_x)) + ", " + str(round(camera_y)) + ") (WASD), " \
        "Pen Size: " + str(pen_size) + " (Z-/X+), " \
        "Pen Color: " + str(pen_color) + " (1/2/3)-"
    
print("\n~~~FILES~~~")
for filename in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")):
    if filename[len(filename) - 4:len(filename)] == ".csv": print(filename)
save_name = input("\nEnter save file name: ").replace(" ", "_").replace(".csv", "")
# gets a save file.

pygame.init()
width, height = 1280, 960
window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
running = True
dt = 60
# initialize program variables.

data = {
    "pen": Pen(10, (0, 0, 0), 0),
    "paint": { 0: [] },
    "paint_trash": {},
    "strokes": 0,
    "camera": Camera(window, 0.0, 0.0, width, height, 1.0),
    "ui": [ Bar(window, 0, 0, width, 25, "MenuBar", (200, 200, 200)) ],
    "keys": { 'z': False, 'x': False, 'c': False, '\\': False, "q": False, "e": False },
    "debug": False
}
data["ui"].append(Text(window, 5, 0, "MenuText", create_menu_text(False, data["camera"].zoom, data["camera"].x, data["camera"].y, data["pen"].size, data["pen"].color), 32, (0, 0, 0)))
# initialize program data.

for element in data["ui"]:
    if element.name == "MenuBar": data["ui"].append(Bar(window, element.width - element.height, 0, element.height, element.height, "ColorBar", (0, 0, 0)))
# pen color indicator.

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves", save_name + ".csv")
if os.path.exists(save_path):
    try:
        with open(save_path, "r") as save:
            csv_reader = csv.DictReader(save)
            for row in csv_reader: data["paint"][0].append(Paint(window, int(row["x_init"]), int(row["y_init"]), int(row["x"]), int(row["y"]), int(row["size"]), (int(row["red"]), int(row["green"]), int(row["blue"]))))
        
        print("Opening save file (" + save_name + ".csv)")
                
    except: 
        print("Save file corrupted. Exiting program. (" + save_name + ".csv)")
        exit()

else: 
    open(save_path, mode="w", newline="")
    print("Opening new save file (" + save_name + ".csv)")
# loads specified save.

old_mouse_x, old_mouse_y = pygame.mouse.get_pos()
data["camera"].set_old()
was_pressed = False

while running:
    key = pygame.key.get_pressed()
    alt_down = key[pygame.K_LALT] or key[pygame.K_RALT]
    # get key press values.

    if key[pygame.K_ESCAPE]: running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    # get program exiting.

    window.fill((255, 255, 255))
    # clears screen.

    fps = clock.get_fps()
    pressed = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for element in data["ui"]:
        if element.name == "MenuBar": mouse_y -= element.height
    # update current tick variables.

    if single_key_press(key[pygame.K_BACKSLASH], data["keys"], "\\"):
        if not data["debug"]: 
            data["debug"] = True
            data["ui"].append(Text(window, 5, height - 32, "DebugText", "Debug: True", 32, (0, 0, 0)))
            data["ui"].append(Text(window, 5, height - 64, "FPSText", "", 32, (0, 0, 0)))

        else: 
            data["debug"] = False
            _removal_list = []
            for i in range(len(data["ui"])):
                if data["ui"][i].name == "DebugText": _removal_list.append(i)
                elif data["ui"][i].name == "FPSText": _removal_list.append(i)

            _removals = 0
            for index in _removal_list:
                data["ui"].pop(index - _removals)
                _removals += 1
    # toggles debug.

    if single_key_press(key[pygame.K_c], data["keys"], "c"):
        if not alt_down:
            if not len(data["paint"]) <= 1:
                data["paint_trash"][data["strokes"]] = data["paint"][data["strokes"]]
                del data["paint"][data["strokes"]]
                data["strokes"] -= 1
        
        elif data["strokes"] + 1 in data["paint_trash"].keys():
            data["strokes"] += 1
            data["paint"][data["strokes"]] = data["paint_trash"][data["strokes"]]
            del data["paint_trash"][data["strokes"]]
    # manages undone paint.
    
    if single_key_press(key[pygame.K_z], data["keys"], "z") and not data["pen"].size <= 1: data["pen"].size -= 1
    if single_key_press(key[pygame.K_x], data["keys"], "x"): data["pen"].size += 1
    # manages pen size. 

    if key[pygame.K_1]: data["pen"].color = (data["pen"].color[0] + ((1 if data["pen"].color[0] < 255 else 0) if not alt_down else (-1 if data["pen"].color[0] > 0 else 0)), 
        data["pen"].color[1], 
        data["pen"].color[2])

    if key[pygame.K_2]: data["pen"].color = (data["pen"].color[0], 
        data["pen"].color[1] + ((1 if data["pen"].color[1] < 255 else 0) if not alt_down else (-1 if data["pen"].color[1] > 0 else 0)), 
        data["pen"].color[2])

    if key[pygame.K_3]: data["pen"].color = (data["pen"].color[0], 
        data["pen"].color[1], 
        data["pen"].color[2] + ((1 if data["pen"].color[2] < 255 else 0) if not alt_down else (-1 if data["pen"].color[2] > 0 else 0)))
    # manages pen colors.

    step = data["camera"].SPEED / data["camera"].zoom * dt * 60
    if key[pygame.K_w]: data["camera"].y -= step
    if key[pygame.K_a]: data["camera"].x -= step
    if key[pygame.K_s]: data["camera"].y += step
    if key[pygame.K_d]: data["camera"].x += step
    if single_key_press(key[pygame.K_q], data["keys"], "q"): data["camera"].zoom_preset -= 1
    if single_key_press(key[pygame.K_e], data["keys"], "e"): data["camera"].zoom_preset += 1
    # update camera position and zoom.

    for element in data["ui"]:
        if element.name == "MenuText": element.set_text(create_menu_text(alt_down, data["camera"].zoom, data["camera"].x, data["camera"].y, data["pen"].size, data["pen"].color))
        elif element.name == "ColorBar": element.color = data["pen"].color
    # update ui elements.

    if pressed:
        if was_pressed: data["paint"][data["strokes"]].append(Paint(
            window,
            round((old_mouse_x - data["camera"].width / 2) / data["camera"].old_zoom + data["camera"].old_x),
            round((old_mouse_y - data["camera"].height / 2) / data["camera"].old_zoom + data["camera"].old_y),
            round((mouse_x - data["camera"].width / 2) / data["camera"].zoom + data["camera"].x),
            round((mouse_y - data["camera"].height / 2) / data["camera"].zoom + data["camera"].y),
            data["pen"].size, data["pen"].color
            ))

        else: 
            data["strokes"] += 1
            data["paint"][data["strokes"]] = []
            data["paint_trash"] = {}
            data["paint"][data["strokes"]].append(Paint(
            window,
            round((mouse_x - data["camera"].width / 2) / data["camera"].zoom + data["camera"].x),
            round((mouse_y - data["camera"].height / 2) / data["camera"].zoom + data["camera"].y),
            round((mouse_x - data["camera"].width / 2) / data["camera"].zoom + data["camera"].x),
            round((mouse_y - data["camera"].height / 2) / data["camera"].zoom + data["camera"].y),
            data["pen"].size, data["pen"].color
            ))
    # adds paint.
            
    was_pressed = pressed
    old_mouse_x, old_mouse_y = mouse_x, mouse_y
    data["camera"].set_old()
    # update last tick variables.

    for element in data["ui"]:
        if element.name == "MenuBar":
            for stroke in data["paint"].keys():
                for line in data["paint"][stroke]: line.render(-data["camera"].x, element.height - data["camera"].y, data["camera"].width, data["camera"].height, data["camera"].zoom, data["debug"])
    # paint rendering.
    
    for element in data["ui"]: 
        if data["debug"] and element.name == "FPSText": element.set_text("FPS: " + str(math.floor(fps)))
        element.render()
    pygame.display.flip()
    dt = clock.tick() / 1000
# end of main loop.

save_data = [["x_init", "y_init", "x", "y", "size", "red", "green", "blue"]]
for stroke in data["paint"].keys():
    for line in data["paint"][stroke]: save_data.append([line.x_init, line.y_init, line.x, line.y, line.size, line.color[0], line.color[1], line.color[2]])
with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(save_data)
# saves data.

pygame.quit()