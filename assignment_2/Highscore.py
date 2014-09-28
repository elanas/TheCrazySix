import pygame

from GameState import GameState
from Globals import Globals
from Menu import Menu

class Highscore(GameState):
    # FADEINTIME = 5.0
    # FADEOUTTIME = 0.2
    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0.0
        Globals.SCREEN.fill(pygame.color.Color("black"))
    
    def render(self):
        font = pygame.font.Font(None, 64)
        surf = font.render("Highscore screen", True, pygame.color.Color("white"))
        width, height = surf.get_size()
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, Globals.HEIGHT / 2 - height / 2 + 64))

        pygame.display.flip()
 
    def update(self, time):
        self.time += time
    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu()
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     Globals.STATE = Menu()