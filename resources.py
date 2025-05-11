import pygame
class Resources:
    pygame.init()
    planet_default_image = pygame.image.load("images/planetbig.png")
    background_image = pygame.image.load("images/background.jpg")
    win_sfx = pygame.mixer.Sound("sounds/jump.wav")