# IMPORT THE PYGAME
import pygame
import random


class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    BACKGROUND_COLOR = (165, 242, 212)
    MENU_BACKGROUND = pygame.image.load("images/menu_background.png")
    INITIAL_BACKGROUND = pygame.image.load("images/menu_background.png")
