import pygame
import random
from asset_loader import AssetLoader


class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    BACKGROUND_COLOR = (165, 242, 212)
    HEALTH_BAR = None
    PLAYER_NAME = None
    PLAYER_SCORE = 0
    INTRO_SOUND_PLAYED = False
    CURRENT_LEVEL = -1
    LEVELS = None
    MENU_SOUND = None
    CUTSCENE_SOUND = None
