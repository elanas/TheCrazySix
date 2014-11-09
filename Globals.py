import pygame
import random
import HealthBar


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

    @staticmethod
    def init_levels():
        import IntroScreen
        import SyringeLevel
        import ZombieLevel
        Globals.CURRENT_LEVEL = -1
        Globals.LEVELS = (
            IntroScreen.IntroScreen(),
            SyringeLevel.SyringeLevel(),
            ZombieLevel.ZombieLevel()
            )

    @staticmethod
    def goto_next_level():
        if Globals.CURRENT_LEVEL + 1 < len(Globals.LEVELS):
            Globals.CURRENT_LEVEL += 1
            Globals.STATE = Globals.LEVELS[Globals.CURRENT_LEVEL]
            Globals.LEVELS[Globals.CURRENT_LEVEL].got_current_state()
            return True
        else:
            return False

    @staticmethod
    def goto_first_level():
        Globals.CURRENT_LEVEL = -1
        Globals.goto_next_level()

    @staticmethod
    def reset_game():
        Globals.CURRENT_LEVEL = -1
        Globals.HEALTH_BAR = None
        Globals.init_levels()
