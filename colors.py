class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    blue = (25, 55, 225)

    light_red = (255, 64, 64)
    dark_red = (128, 0, 0)
    light_green = (64, 255, 64)
    dark_green = (0, 128, 0)    

    yellow = (196, 196, 0)
    orange = (255, 127, 0)
    purple = (127, 0, 255)
    pink = (255, 16, 196)
    turquoise = (0, 255, 255)
    good_color = (32, 255, 168)
    cyan = turquoise
    tan = (210, 180, 140)

    brown = (139,69,19)
    brown = (139,69,19)
    brown = (150,75,0)

    gray = (128, 128, 128)
    dark_gray = (64, 64, 64)
    light_gray = (192, 192, 192)
    light_blue = (102, 178, 255)
    dark_blue = (0, 0, 192)

    def set_luminosity(color: tuple[int, int, int], luminosity: int):
        # if luminosity > 255 or luminosity < 0:
        #     raise Exception
        mult = min(255/max(color), luminosity/Colors.get_luminosity(color))
        return (min(255, color[0]*mult), min(255, color[1]*mult), min(255, color[2]*mult))
    
    def get_luminosity(color: tuple[int, int, int]) -> int:
        return sum(color)//3