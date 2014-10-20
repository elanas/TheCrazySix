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
    PLAYER_NAME = None
    PLAYER_HEALTH = 100
    REMAINING_TIME = 30000
    PLAYER_SCORE = 0 # Change the score