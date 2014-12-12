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
    EVENTS_UP = []
    EVENTS_DOWN = []
    EVENTS_LEFT = []
    EVENTS_RIGHT = []
    EVENTS_ACTION = []
    EVENTS_ESCAPE = []
    EVENTS_RETURN = []
    EVENTS_BACKSPACE = []

    @staticmethod
    def init_event_keys():
        from EventPair import EventPair
        Globals.EVENTS_UP = [EventPair(type=pygame.KEYDOWN, value=pygame.K_UP), EventPair(type=pygame.JOYHATMOTION, hat=0, value=(0, 1))]
        Globals.EVENTS_DOWN = [EventPair(type=pygame.KEYDOWN, value=pygame.K_DOWN), EventPair(type=pygame.JOYHATMOTION, hat=0, value=(0, -1))]
        Globals.EVENTS_LEFT = [EventPair(type=pygame.KEYDOWN, value=pygame.K_LEFT), EventPair(type=pygame.JOYHATMOTION, hat=0, value=(-1, 0))]
        Globals.EVENTS_RIGHT = [EventPair(type=pygame.KEYDOWN, value=pygame.K_RIGHT), EventPair(type=pygame.JOYHATMOTION, hat=0, value=(1, 0))]
        Globals.EVENTS_ACTION = [EventPair(type=pygame.KEYDOWN, value=pygame.K_SPACE), EventPair(type=pygame.JOYBUTTONDOWN, value=0)]
        Globals.EVENTS_ESCAPE = [EventPair(type=pygame.KEYDOWN, value=pygame.K_ESCAPE), EventPair(type=pygame.JOYBUTTONDOWN, value=6)]
        Globals.EVENTS_RETURN = [EventPair(type=pygame.KEYDOWN, value=pygame.K_RETURN), EventPair(type=pygame.JOYBUTTONDOWN, value=3)]
        Globals.EVENTS_BACKSPACE = [EventPair(type=pygame.KEYDOWN, value=pygame.K_BACKSPACE)]
