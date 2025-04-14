import math
from ui import Camera
from colors import Colors
import pygame
from pygame import gfxdraw
class GameObject:
    #self.x: float -> "class variables" or smth cuz you dont want to be able to make a gameObject
    def __init__(self) -> None:
        self.x: float = 0
        self.y: float = 0
        self.size: int = 10

    def draw(self) -> None:
        raise NotImplementedError

    def tick(self) -> None:
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
        self.radius: float = 0

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
        pygame.gfxdraw.filled_circle(camera.window, int(self.x/camera.scale+camera.x), int(self.y/camera.scale+camera.y), int(self.radius/camera.scale+.5), self.color)
        if aa:
            pygame.gfxdraw.aacircle(camera.window, int(self.x/camera.scale+camera.x), int(self.y/camera.scale+camera.y), int(self.radius/camera.scale+.5), (int(self.color[0]/1.5), int(self.color[1]/1.5), int(self.color[2]/1.5)))
        if shine:
            pygame.draw.circle(camera.window, Colors.white, (int(self.x/camera.scale+camera.x), int(self.y/camera.scale+camera.y)), int((self.radius*0.8)/camera.scale+.5), int(self.radius/camera.scale/5), draw_top_right=True)
    def tick(self):
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




