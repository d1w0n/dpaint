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
    if not alt_keys: return "Zoom: " + str(round(camera_zoom * 100)) + "% (Q-/E+), " \
        "Position: (" + str(round(camera_x)) + ", " + str(round(camera_y)) + ") (WASD), " \
        "Size: " + str(pen_size) + " (Z-/X+), " \
        "Color: " + str(pen_color) + " (1/2/3)+" # TODO position should display mouse x, y
    
    else: return "Zoom: " + str(round(camera_zoom * 100)) + "% (Q-/E+), " \
        "Position: (" + str(round(camera_x)) + ", " + str(round(camera_y)) + ") (WASD), " \
        "Size: " + str(pen_size) + " (Z-/X+), " \
        "Color: " + str(pen_color) + " (1/2/3)-"

def false_dict_constructor(*args) -> dict:
    _dict = {}
    for value in args: _dict[value] = False
    return _dict
# creates a dict of false values (for key input.)
