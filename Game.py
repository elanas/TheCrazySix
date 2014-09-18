# IMPORT THE PYGAME
import pygame

from Player import Player

pygame.init()

BACKGROUND_IMAGE_NAME = "test.png"

background = pygame.image.load(BACKGROUND_IMAGE_NAME)
size = background.get_size()
screen = pygame.display.set_mode(size)
frames_per_second = 24

pygame.quit()
