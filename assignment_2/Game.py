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

MIN_UPDATE_INTERVAL = .05


# class Highscore(GameState):
#     # FADEINTIME = 5.0
#     # FADEOUTTIME = 0.2
#     def __init__(self):
#         GameState.__init__(self)
#         self.color = pygame.color.Color("black")
#         self.time = 0.0
#         Globals.SCREEN.fill(pygame.color.Color("black"))
    
#     def render(self):
#         font = pygame.font.Font(None, 64)
#         surf = font.render("Highscore screen", True, pygame.color.Color("white"))
#         width, height = surf.get_size()
#         Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, Globals.HEIGHT / 2 - height / 2 + 64))

#         pygame.display.flip()
 
#     def update(self, time):
#         self.time += time
#     def event(self, event):
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             Globals.STATE = Menu()
#             print "should change to menu"
#         # elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#         #     Globals.STATE = Menu()


# >>>>>>> 548dd95d1f22a2e6b04292e74af33a7ebbd2d324
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
