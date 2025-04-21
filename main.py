import pygame
from colors import Colors
import body
from camera import Camera
from level import Level
import copy

class Game:
    def __init__(self):
        pygame.init()


        # Settings
        self.background_color: tuple[int, int, int] = Colors.black

        self.screen_width: int = 1280
        self.screen_height: int = 720

        self.target_fps: int = 60
        # Implement vSync later, supported by pygame


        # Create Objects
        self.objects: list[body.GameObject] = []
        self.player = body.Player()
        self.planet = body.Planet()
        self.planet2 = body.Planet()
        self.planet2.x = 100
        self.planet2.y = 50
        self.player.x = 75

        #self.objects.append(self.player)
        #self.objects.append(self.planet)
        #self.objects.append(self.planet2)

        level: Level = Level()
        level.addObject(self.player)
        level.addObject(self.planet)
        level.addObject(self.planet2)

        self.window: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.camera: Camera = Camera(self.window)

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.load_level(level)


        self.running: bool = True
        while self.running:
            
            self.window.fill(self.background_color)


            # Get User Input
            self.events: list[pygame.event.Event] = pygame.event.get()
            for event in self.events:        
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        break
                
                    if event.key == pygame.K_UP:
                        self.camera.set_scale(self.camera.scale+.05)

                    elif event.key == pygame.K_DOWN:
                        self.camera.set_scale(self.camera.scale-.05)


                if event.type == pygame.MOUSEWHEEL:
                    x, y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                    scale = self.camera.scale
                    mult = event.y/20
                    scale *= 1-mult
                    if scale <= 0.1:
                        scale = 0.1
                    else:
                        self.camera.set_scale(scale)
                        self.camera.x -= x*mult/scale
                        self.camera.y -= y*mult/scale



            # Tick game logic
            self.tick(1/self.target_fps)
            x, y = self.camera.get_screen_pos(pygame.mouse.get_pos())
            self.player.x = x
            self.player.y = y

            # Draw game
            self.draw()

            pygame.display.flip()

            self.clock.tick(self.target_fps)


        pygame.quit()

    def all_pair(objects: list, func) -> None: #Calls function with all pairs of data set
        for i in range(len(objects)):
            obj1 = objects[i]
            for j in range(i+1, len(objects)):
                obj2 = objects[j]
                func(obj1, obj2)

    def tick(self, dt: float):
        Game.all_pair([object for object in self.objects if isinstance(object, body.Body)], body.Body.apply_gravity)
        for object in self.objects:
            object.tick(dt)

    def draw(self):
        for object in self.objects:
            object.draw(self.camera)

    def load_level(self, level: Level):
        self.objects = copy.deepcopy(level.objects)
        self.camera.set_scale(self.screen_height/level.size)

def main():
    game = Game()

if __name__ == "__main__":
    main()