# IMPORT THE PYGAME
import pygame
import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


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
    USE_BRIGHTNESS = False
    BRIGHTNESS_SURF = None
    PLAYING_MENU_SOUND = False
    HUD_MANAGER = None
    DISORIENTED = False
    DISORIENTED_SURF = None
    DISORIENTED_COLOR_SUB = (0, 70, 70)
    EVENT_MANAGER = None
