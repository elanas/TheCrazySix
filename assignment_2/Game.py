# IMPORT THE PYGAME
import pygame
import random
import pygame.color
import pygame.font

from GameState import GameState
from Globals import Globals
from MainGame import MainGame
from Title import Title
import sys

def initialize():
    pygame.init()
    Globals.WIDTH = 700
    Globals.HEIGHT = 500
    Globals.SCREEN = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    Globals.STATE = Title()
    # Globals.STATE = MainGame()

def loadGame():
    pass

def loop():
    while Globals.RUNNING:
        last = pygame.time.get_ticks()

        Globals.STATE.render()
        pygame.display.flip()

        elapsed = (pygame.time.get_ticks() - last) / 1000.0
        Globals.STATE.update(elapsed)

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
