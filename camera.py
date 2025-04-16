
class Camera:
    def __init__(self, window) -> None:
        self.window = window
        self.width, self.height = self.window.get_size()

        self.x = 0
        self.y = 0

        self.scale = 1

    
    def set_pos(self, x, y) -> None:
        self.target_x = x
        self.target_y = y

    def set_scale(self, scale) -> None:
        self.target_scale = scale
 

    def get_x(self, x) -> int:
        return round((x+self.width/2)*self.scale+self.x)

    def get_y(self, y) -> int:
        return round((y+self.height/2)*self.scale+self.y)

    def get_screen_x(self, x) -> int:
        return round((x-self.x)/self.scale-self.width/2)

    def get_screen_y(self, y) -> int:
        return round((y-self.y)/self.scale-self.height/2)
    
    def get_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        return self.get_screen_x(pos[0]), self.get_screen_y(pos[1])      