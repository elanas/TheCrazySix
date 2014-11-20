# IMPORT THE PYGAME
import pygame
import random
import pygame.color
import pygame.font

from GameState import GameState
from Globals import Globals
# from MainGame import MainGame
# from Title import Title
from CustomLevelPicker import CustomLevelPicker
import sys

MIN_UPDATE_INTERVAL = .05


def initialize():
    pygame.init()
    Globals.WIDTH = 1000
    Globals.HEIGHT = 600
    Globals.SCREEN = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    Globals.STATE = CustomLevelPicker()
    pygame.display.set_caption('The Crazy Six - Field Day')


def loadGame():
    pass


def loop():
    time_elapsed = 0
    while Globals.RUNNING:
        last = pygame.time.get_ticks()

        Globals.STATE.render()
        pygame.display.flip()

        elapsed = (pygame.time.get_ticks() - last) / 1000.0
        time_elapsed += elapsed
        if time_elapsed >= MIN_UPDATE_INTERVAL:
            Globals.STATE.update(time_elapsed)
            time_elapsed -= MIN_UPDATE_INTERVAL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.RUNNING = False
            else:
                Globals.STATE.event(event)


def main():
    initialize()
    # loadGame()
    loop()


if __name__ == '__main__':
    main()
