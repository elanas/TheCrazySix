# IMPORT THE PYGAME
import pygame
import random
import pygame.color
import pygame.font

from GameState import GameState
from Globals import Globals
# from MainGame import MainGame
from Title import Title
from SettingsManager import SettingsManager
import sys
from EventHandler import EventHandler
from EventManager import EventManager

MIN_UPDATE_INTERVAL = .05


class Game(EventHandler):

    def __init__(self):
        self.initialize()
        self.loop()

    def initialize(self):
        pygame.init()
        Globals.WIDTH = 1000
        Globals.HEIGHT = 600
        Globals.SCREEN = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
        SettingsManager.load()
        Globals.set_brightness(SettingsManager.BRIGHTNESS, save=False)
        Globals.set_volume(SettingsManager.VOLUME, save=False)
        pygame.display.set_caption('The Crazy Six - Field Day')
        Globals.STATE = Title()
        Globals.init_event_keys()
        Globals.EVENT_MANAGER = EventManager()

    def loop(self):
        time_elapsed = 0
        while Globals.RUNNING:
            last = pygame.time.get_ticks()

            Globals.STATE.render()
            if Globals.USE_BRIGHTNESS:
                Globals.SCREEN.blit(Globals.BRIGHTNESS_SURF, (0, 0))
            pygame.display.flip()
            Globals.EVENT_MANAGER.check_events()

            elapsed = (pygame.time.get_ticks() - last) / 1000.0
            time_elapsed += elapsed
            if time_elapsed >= MIN_UPDATE_INTERVAL:
                Globals.STATE.update(time_elapsed)
                time_elapsed -= MIN_UPDATE_INTERVAL


if __name__ == '__main__':
    game = Game()
