import numpy as np
import math

def pixels_to_mm(coordinates):
    
    dolzina_enega_kvadratka_piksli = math.sqrt(pow((119-59),2) + pow((62-63),2))
    coord_v_mm = np.array([])
    for coordinate in coordinates:
        x_mm = (coordinate[0]/dolzina_enega_kvadratka_piksli) * 24
        y_mm = (coordinate[1]/dolzina_enega_kvadratka_piksli) * 24

        coord_v_mm = np.append(x_mm, y_mm)

    return coord_v_mm

# x,y = [[63,119]]
def transformacija(stare_koord):
    x = stare_koord[0]
    y = stare_koord[1]
    xn = x - 65
    yn = -y+415
    novi = [[xn,yn]]
    novi_v_mm = pixels_to_mm(novi)

    return novi_v_mm