import pygame
import random
import HealthBar
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
    VOLUME = 1.0
    BRIGHTNESS = 1.0

    @staticmethod
    def init_levels():
        from Levels import IntroScreen
        from Levels import SyringeLevel
        from Levels import ZombieLevel
        from Levels import ZombieCutScene
        from Levels import PostZombieCutScene
        Globals.CURRENT_LEVEL = -1
        Globals.LEVELS = (
            IntroScreen.IntroScreen(),
            SyringeLevel.SyringeLevel(),
            ZombieLevel.ZombieLevel(),
            ZombieCutScene.ZombieCutScene(),
            PostZombieCutScene.PostZombieCutScene()
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
    def play_menu_sound():
        if Globals.MENU_SOUND is None:
            loader = AssetLoader(sound_path_start='sounds')
            Globals.MENU_SOUND = loader.load_sound('menu_music.ogg')
        if Globals.MENU_SOUND.get_num_channels() > 0:
            return
        Globals.MENU_SOUND.play(loops=-1)

    @staticmethod
    def stop_menu_sound():
        if Globals.MENU_SOUND is not None:
            Globals.MENU_SOUND.stop()

    @staticmethod
    def goto_first_level():
        Globals.CURRENT_LEVEL = -1
        Globals.goto_next_level()

    @staticmethod
    def reset_game():
        Globals.CURRENT_LEVEL = -1
        Globals.HEALTH_BAR = None
        Globals.TIME = None
        Globals.init_levels()
