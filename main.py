import pygame
from colors import Colors
import game
from camera import Camera

def main():

    pygame.init()


    # Settings
    background_color: tuple[int, int, int] = Colors.black

    screen_width: int = 1280
    screen_height: int = 720

    target_fps: int = 60
    # Implement vSync later, supported by pygame


    # Create Objects
    objects: list[game.GameObject] = []
    player = game.Player()
    objects.append(player)

    window: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    camera: Camera = Camera(window)

    clock: pygame.time.Clock = pygame.time.Clock()

    running: bool = True
    while running:
        
        window.fill(background_color)


        # Get User Input
        events: list[pygame.event.Event] = pygame.event.get()
        for event in events:        
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break


        # Tick game logic
        tick(objects, 1/target_fps)
        x, y = camera.get_screen_pos(pygame.mouse.get_pos())
        player.x = x
        player.y = y

        # Draw game
        draw(objects, camera)

        pygame.display.flip()

        clock.tick(target_fps)


    pygame.quit()


def tick(objects: list[game.GameObject], dt: float):
    for object in objects:
        object.tick(dt)

def draw(objects: list[game.GameObject], camera: Camera):
    for object in objects:
        object.draw(camera)



main()