import pygame
class Resources:
    pygame.init()
    planet_default_image = pygame.image.load("images/planetbig.png")
    background_image = pygame.image.load("images/background.jpg")
    win_sfx = pygame.mixer.Sound("sounds/win.wav")
    collide_sfx = pygame.mixer.Sound("sounds/collide.wav")
    music = pygame.mixer.music.load("music/482139.mp3")