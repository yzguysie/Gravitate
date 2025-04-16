import math
from camera import Camera
from colors import Colors
import pygame
import pygame.gfxdraw

class GameObject:
    #self.x: float -> "class variables" or smth cuz you dont want to be able to make a gameObject
    def __init__(self) -> None:
        self.x: float = 0
        self.y: float = 0
        self.size: int = 10

    def draw(self, camera: Camera) -> None:
        raise NotImplementedError

    def tick(self, dt: float) -> None:
        raise NotImplementedError
    
    def isColliding(self, other: 'GameObject') -> bool:
        return (self.x-other.x)**2 + (self.y-other.y)**2 < (self.size+other.size)**2

class Body(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.static: bool = None
        self.x_vel: float = 0
        self.y_vel: float = 0
        self.mass: float = 0
        self.radius: float = 10
        self.color: tuple[int, int, int] = Colors.blue

    def distance_to(self, other: 'Body') -> float:
        return math.sqrt(abs(self.x-other.x)**2+abs(self.y-other.y)**2)

    def calc_gravity(self, other: 'Body') -> tuple[float, float]:
        # Returns force of gravity as a tuple vector containing x force and y force
        G = 1 # Gravitational Constant
        distance = self.distance_to(other)
        if distance == 0:
            print("WARNING: DIVISION BY 0 in calc_gravity (distance = 0)")
            return (0, 0)

        

        angle = math.atan2(self.y - other.y, self.x - other.x)
        vector = (math.cos(angle), math.sin(angle))


        force = ((self.mass*other.mass)/distance**2)
        return (vector[0]*force*G, vector[1]*force*G)
    
    def is_visible(self, camera: Camera, screen_width, screen_height) -> bool: # Returns whether the object would be visible, if drawn
        return abs(self.x/camera.scale+camera.x) < screen_width+self.radius/camera.scale and abs(self.y/camera.scale+camera.y) < screen_height+self.radius/camera.scale
    
    def draw(self, camera: Camera, aa=True, shine=True):
        pygame.gfxdraw.filled_circle(camera.window, camera.get_x(self.x), camera.get_y(self.y), round(self.radius/camera.scale), self.color)
        if aa:
            pygame.gfxdraw.aacircle(camera.window, camera.get_x(self.x), camera.get_y(self.y), round(self.radius/camera.scale), (Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)/1.5)))
        if shine:
            pygame.draw.circle(camera.window, Colors.white, (camera.get_x(self.x), camera.get_y(self.y)), round((self.radius*0.8)/camera.scale), round(self.radius/camera.scale/5), draw_top_right=True)
    
    def tick(self, dt: float):
        pass
        
class Player(Body):
    def __init__(self) -> None:
        super().__init__()
        self.launched: bool = False # Whether or not the player has been launched and should be affected by objects

class BlackHole(Body):
    def __init__(self) -> None:
        super().__init__()
        self.static: bool = True
    
    def consume(other: Body) -> None:
        pass

class Target(BlackHole):
    def __init__(self) -> None:
        super().__init__()

class Planet(Body):
    def __init__(self) -> None:
        super().__init__()

class Star(Body):
    def __init__(self) -> None:
        super().__init__()




