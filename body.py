import math
from camera import Camera
from colors import Colors
import pygame
import pygame.gfxdraw
from resources import Resources

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, centered: bool = True) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x: int = 0
        self.y: int = 0
        self.centered: bool = centered
        self.width: int = 100
        self.height: int = 100
        self.source_image: pygame.surface.Surface = image
        self.image: pygame.surface.Surface = image
        self.rect: pygame.rect.Rect = self.image.get_rect()

    def set_size(self, width: int, height: int) -> None:
        if self.width == width and self.height == height:
            return
        self.width = width
        self.height = height
        self.image = pygame.transform.smoothscale(self.source_image, (round(width), round(height)))
        self.rect = self.image.get_rect()

    def draw(self, surface: pygame.surface.Surface) -> None:
        if self.centered:
            surface.blit(self.image, (self.x-self.image.get_width()/2, self.y-self.image.get_height()/2))
        else:
            surface.blit(self.image, (self.x, self.y))         


class GameObject:
    #self.x: float -> "class variables" or smth cuz you dont want to be able to make a gameObject
    def __init__(self) -> None:
        self.x: float = 0
        self.y: float = 0
        self.size: int = 10

    def calc_distance(point1: tuple, point2: tuple) -> float:
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    
    def draw(self, camera: Camera) -> None:
        raise NotImplementedError

    def tick(self, dt: float) -> None:
        raise NotImplementedError
    
    def is_colliding(self, other: 'GameObject') -> bool:
        return (self.x-other.x)**2 + (self.y-other.y)**2 < (self.size+other.size)**2
    
    def get_overlap(self, other: 'GameObject') -> float:
        return (self.size+other.size) - math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
    
    def to_str(self, separator: str) -> str:
        data = [type(self), self.x, self.y, self.size]
        return data.join(separator)
    
    def from_str(string: str, separator: str) -> 'GameObject':
        obj = GameObject()
        data = string.split(separator)
        print(data)
        obj_type = data[0]

        if obj_type == "Player":
            return Player.from_str(string, separator)
        
        if obj_type == "Target":
            return Target.from_str(string, separator)

        if obj_type == "Planet":
            return Planet.from_str(string, separator)
        
        if obj_type == "Star":
            return Star.from_str(string, separator)
        print(obj_type)
        
        return None

    def vector_to(self, other: 'GameObject') -> tuple[float, float]:
        angle = math.atan2(other.y - self.y, other.x - self.x)
        return (math.cos(angle), math.sin(angle))


class Body(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.static: bool = None
        self.xvel: float = 0
        self.yvel: float = 0
        self.mass: float = 10
        self.radius: float = 10
        self.color: tuple[int, int, int] = Colors.blue
        self.sprite = None

    def make_sprite(self, image) -> None:
        self.sprite = Sprite(image)
        self.sprite.set_size(self.radius, self.radius)

    def getting_closer(self, other: 'Body') -> bool:
        distance_1 = GameObject.calc_distance((self.x, self.y), (other.x, other.y))
        distance_2 = GameObject.calc_distance((self.x+self.xvel*.01, self.y+self.yvel*.01), (other.x+other.xvel*.01, other.y+other.yvel*.01))
        return distance_2 <= distance_1

    def distance_to(self, other: 'Body') -> float:
        return math.sqrt(abs(self.x-other.x)**2+abs(self.y-other.y)**2)

    def calc_gravity(self, other: 'Body', G: float = 1) -> tuple[float, float]:
        # Returns force of gravity as a tuple vector containing x force and y force
        distance = self.distance_to(other)
        if distance == 0:
            print("WARNING: DIVISION BY 0 in calc_gravity (distance = 0)")
            return (0, 0)

        

        #angle = math.atan2(other.y - self.y, other.x - self.x)
        #vector = (math.cos(angle), math.sin(angle))
        vector = self.vector_to(other)


        force = ((self.mass*other.mass)/distance**2)
        return (vector[0]*force*G, vector[1]*force*G)
    
    def apply_gravity(body1: 'Body', body2: 'Body', G: float = 10) -> None:
        force: tuple[float, float] = body1.calc_gravity(body2, G)
        if not body1.static:
            body1.xvel += force[0]/body1.mass
            body1.yvel += force[1]/body1.mass
        if not body2.static:
            body2.xvel -= force[0]/body2.mass
            body2.yvel -= force[1]/body2.mass

    def apply_collision(body1: 'Body', body2: 'Body') -> None:
        if not body1.is_colliding(body2):
            return
        
        if not body1.getting_closer(body2):
            print("Nope")
            return
        

        if body1.static and body2.static:
            return
        if type(body1) == Player and type(body2) == Target:
            body1.reached_target = True

        if type(body1) == Target and type(body2) == Player:
            body2.reached_target = True
        # vector: tuple[float, float] = body1.vector_to(body2)
        # overlap: float = body1.get_overlap(body2)
        # b1mult: float = body1.mass/(body1.mass+body2.mass)
        # b2mult: float = body2.mass/(body1.mass+body2.mass)
        # if body1.static: # Apply all force and movement to non-static if one body is static
        #     b1mult = 0
        #     b2mult = 1
        # if body2.static:
        #     b1mult = 1
        #     b2mult = 0

        phi = math.atan2(body2.y - body1.y, body2.x - body1.x)
        theta1 = math.atan2(body1.yvel, body1.xvel)
        theta2 = math.atan2(body2.yvel, body2.xvel)
        v1 = math.sqrt(body1.xvel**2+body1.yvel**2)
        v2 = math.sqrt(body2.xvel**2+body2.yvel**2)
        m1 = body1.mass
        m2 = body2.mass
        pi = math.pi
        
        if not body1.static and not body2.static:
            velb1thing = (v1*math.cos(theta1-phi)*(m1-m2) + 2*m2*v2*math.cos(theta2-phi))/(m1+m2)
            velb2thing = (v2*math.cos(theta2-phi)*(m2-m1) + 2*m1*v1*math.cos(theta1-phi))/(m1+m2)



        elif body1.static:
            velb1thing = 0

            velb2thing = (v2*math.cos(theta2-phi)*(-1))

        else:
            velb1thing = (v1*math.cos(theta1-phi)*(-1))
            velb2thing = 0 


            xvelb1 = velb1thing * (math.cos(phi)+v1*math.sin(theta1-phi)*math.cos(phi+pi/2))
            yvelb1 = velb1thing * (math.sin(phi)+v1*math.sin(theta1-phi)*math.sin(phi+pi/2))
            xvelb2 = velb2thing * (math.cos(phi)+v2*math.sin(theta2-phi)*math.cos(phi+pi/2))
            yvelb2 = velb2thing * (math.sin(phi)+v2*math.sin(theta2-phi)*math.sin(phi+pi/2))
            body1.xvel = xvelb1
            body1.yvel = yvelb1
            body2.xvel = xvelb2
            body2.yvel = yvelb2

        Resources.win_sfx.play()
        # if not body1.static:
        #     body1.x -= overlap*vector[0]*b1mult
        #     body1.y -= overlap*vector[1]*b1mult
        #     print(vector)

        # if not body2.static:
        #     body2.x += overlap*vector[0]*b2mult
        #     body2.y += overlap*vector[1]*b2mult
        
    
    def is_visible(self, camera: Camera, screen_width, screen_height) -> bool: # Returns whether the object would be visible, if drawn
        return abs(self.x/camera.scale+camera.x) < screen_width+self.radius/camera.scale and abs(self.y/camera.scale+camera.y) < screen_height+self.radius/camera.scale
    
    def draw(self, camera: Camera, aa=True, shine=True) -> None:
        if self.sprite:
            self.sprite.x = camera.get_x(self.x)
            self.sprite.y = camera.get_y(self.y)
            if self.sprite.width != self.radius*2/camera.scale:
                self.sprite.set_size(self.radius*2/camera.scale, self.radius*2/camera.scale)
                print("rescale")
            self.sprite.draw(camera.window)
        else:
            pygame.gfxdraw.filled_circle(camera.window, camera.get_x(self.x), camera.get_y(self.y), round(self.radius/camera.scale), self.color)
            if aa:
                pygame.gfxdraw.aacircle(camera.window, camera.get_x(self.x), camera.get_y(self.y), round(self.radius/camera.scale), (Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)/1.5)))
            if shine:
                pygame.draw.circle(camera.window, Colors.white, (camera.get_x(self.x), camera.get_y(self.y)), round((self.radius*0.8)/camera.scale), round(self.radius/camera.scale/5), draw_top_right=True)
        
    def tick(self, dt: float) -> None:
        if not self.static:
            self.x += self.xvel
            self.y += self.yvel

    def to_str(self, separator: str) -> str:
        data = [str(type(self).__name__), str(self.x), str(self.y), str(self.mass), str(self.radius)]
        return separator.join(data)
        
    def from_str(string: str, separator: str):
        data = string.split(separator)
        object = Body()
        object.x = int(data[1])
        object.y = int(data[2])
        object.mass = float(data[3])
        object.radius = float(data[4])
        return object


class Player(Body):
    def __init__(self) -> None:
        super().__init__()
        self.launched: bool = False # Whether or not the player has been launched and should be affected by objects
        self.reached_target: bool = False

    def tick(self, dt: float) -> None:
        self.static = not self.launched
        super().tick(dt)
    
    def from_str(string: str, separator: str):
        data = string.split(separator)
        object = Player()
        object.x = int(data[1])
        object.y = int(data[2])
        object.mass = float(data[3])
        object.radius = float(data[4])
        return object


class BlackHole(Body):
    def __init__(self) -> None:
        super().__init__()
        self.static: bool = True
        self.color = [15, 15, 15]

    def draw(self, camera: Camera) -> None:
        super().draw(camera, aa=True, shine=False)
    
    def consume(self, other: Body) -> None:
        self.mass += other.mass
        self.radius = self.mass**1/2
    
    def from_str(string: str, separator: str):
        data = string.split(separator)
        object = BlackHole()
        object.x = int(data[1])
        object.y = int(data[2])
        object.mass = float(data[3])
        object.radius = float(data[4])
        return object


class Target(BlackHole):
    def __init__(self) -> None:
        super().__init__()
        self.color = [45, 15, 45]
        self.static = True

    def from_str(string: str, separator: str):
        data = string.split(separator)
        object = Target()
        object.x = int(data[1])
        object.y = int(data[2])
        object.mass = float(data[3])
        object.radius = float(data[4])
        return object


class Planet(Body):
    def __init__(self) -> None:
        super().__init__()
        self.color = Colors.tan
        self.static = False
        self.sprite = Sprite(Resources.planet_default_image)

    def from_str(string: str, separator: str):
        data = string.split(separator)
        planet = Planet()
        planet.x = int(data[1])
        planet.y = int(data[2])
        planet.mass = float(data[3])
        planet.radius = float(data[4])
        return planet


class Star(Body):
    def __init__(self) -> None:
        super().__init__()
        self.color = Colors.yellow
        self.static = True

    def from_str(string: str, separator: str):
        data = string.split(separator)
        object = Star()
        object.x = int(data[1])
        object.y = int(data[2])
        object.mass = float(data[3])
        object.radius = float(data[4])
        return object

