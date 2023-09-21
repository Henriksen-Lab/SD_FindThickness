'''
base on this website:
https://stackoverflow.com/questions/36618882/methodology-to-convert-rgb-to-wavelength
'''
def rgb2hsv(r, g, b):
    MAX_PIXEL_VALUE = 255.0
    r = r / MAX_PIXEL_VALUE
    g = g / MAX_PIXEL_VALUE
    b = b / MAX_PIXEL_VALUE
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    v = max_val
    if max_val == 0.0:
        s = 0
        h = 0
    elif (max_val - min_val) == 0.0:
        s = 0
        h = 0
    else:
        s = (max_val - min_val) / max_val
        if max_val == r:
            h = 60 * ((g - b) / (max_val - min_val)) + 0
        elif max_val == g:
            h = 60 * ((b - r) / (max_val - min_val)) + 120
        else:
            h = 60 * ((r - g) / (max_val - min_val)) + 240
    if h < 0:
        h = h + 360.0
    h = h / 2
    s = s * MAX_PIXEL_VALUE
    v = v * MAX_PIXEL_VALUE
    return h, s, v

def hue2wavelength(hue):
    wavelength = 650 - 250 / 270 * hue
    return wavelength

def rgb2wavelength(r,g,b):
    h,s,v = rgb2hsv(r,g,b)
    wavelength = hue2wavelength(h)
    return wavelength