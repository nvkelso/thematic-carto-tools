# http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def rgb_string_to_hex(rgb_string):
    #"rgb(153,153,153)"
    rgb_list = rgb_string[4:-1].split(',')
    for i in range(len(rgb_list)):
        rgb_list[i] = int(rgb_list[i])
    rgb_tuple = tuple( rgb_list )
    return rgb_to_hex(rgb_tuple)

# Unit tests
#hex_to_rgb("#ffffff")             #==> (255, 255, 255)
#hex_to_rgb("#ffffffffffff")       #==> (65535, 65535, 65535)
#rgb_to_hex((255, 255, 255))       #==> '#ffffff'
#rgb_to_hex((65535, 65535, 65535)) #==> '#ffffffffffff'
#rgb_string_to_hex("rgb(247,252,185)") #==> '#'