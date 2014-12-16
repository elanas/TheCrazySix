from __future__ import division
import pygame
import random
import HealthBar
from asset_loader import AssetLoader
from SettingsManager import SettingsManager


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

    @staticmethod
    def get_disoriented_surf():
        if Globals.DISORIENTED_SURF is None:
            Globals.DISORIENTED_SURF = pygame.Surface(
                Globals.SCREEN.get_rect().size).convert()
            Globals.DISORIENTED_SURF.fill(Globals.DISORIENTED_COLOR_SUB)
        return Globals.DISORIENTED_SURF

    @staticmethod
    def init_levels():
        from Levels import IntroScreen
        from Levels import SyringeLevel
        from Levels import ZombieLevel
        from Levels import ZombieCutScene
        from Levels import PostZombieCutScene
        from Levels import BossLevel
        Globals.CURRENT_LEVEL = -1
        Globals.LEVELS = (
            IntroScreen.IntroScreen(),
            SyringeLevel.SyringeLevel(),
            ZombieLevel.ZombieLevel(),
            ZombieCutScene.ZombieCutScene(),
            PostZombieCutScene.PostZombieCutScene(),
            BossLevel.BossLevel()
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
    def goto_previous_level():
        if Globals.CURRENT_LEVEL > 0 and len(Globals.LEVELS) > 1:
            Globals.CURRENT_LEVEL -= 1
            Globals.LEVELS[Globals.CURRENT_LEVEL].got_state_back()
            Globals.STATE = Globals.LEVELS[Globals.CURRENT_LEVEL]
            return True
        else:
            return False

    @staticmethod
    def play_menu_sound():
        if Globals.MENU_SOUND is None:
            loader = AssetLoader(sound_path_start='sounds')
            Globals.MENU_SOUND = loader.load_sound('menu_music.ogg')
        if Globals.PLAYING_MENU_SOUND:
            return
        Globals.MENU_SOUND.play(loops=-1)
        Globals.PLAYING_MENU_SOUND = True

    @staticmethod
    def stop_menu_sound():
        if Globals.PLAYING_MENU_SOUND:
            Globals.MENU_SOUND.stop()
            Globals.PLAYING_MENU_SOUND = False

    @staticmethod
    def goto_first_level():
        Globals.CURRENT_LEVEL = -1
        Globals.goto_next_level()

    @staticmethod
    def reset_game():
        Globals.DISORIENTED = False
        Globals.CURRENT_LEVEL = -1
        Globals.HEALTH_BAR = None
        Globals.HUD_MANAGER = None
        Globals.INTRO_SOUND_PLAYED = False
        Globals.TIME = None
        Globals.init_levels()

    @staticmethod
    def set_volume(volume, save=True):
        if save:
            SettingsManager.set_volume(volume)
        AssetLoader.set_volume(volume / 100)

    @staticmethod
    def set_brightness(brightness, save=True):
        if Globals.BRIGHTNESS_SURF is None:
            Globals.BRIGHTNESS_SURF = \
                pygame.Surface((Globals.WIDTH, Globals.HEIGHT))
            Globals.BRIGHTNESS_SURF.fill((0, 0, 0))
        if save:
            SettingsManager.set_brightness(brightness)
        if SettingsManager.BRIGHTNESS == 100:
            Globals.USE_BRIGHTNESS = False
        else:
            Globals.USE_BRIGHTNESS = True
            Globals.BRIGHTNESS_SURF.set_alpha(
                int((1 - brightness / 100) * 255))
