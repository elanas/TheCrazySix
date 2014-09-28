import pygame

from GameState import GameState
from Globals import Globals
from MainGame import MainGame

class Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0
        Globals.SCREEN.fill(pygame.color.Color("black"))
        self.selection = 0
    
    def render(self):
        font = pygame.font.Font(None, 64)
        surf = font.render("MENU", True, pygame.color.Color("red"))
        width, height = surf.get_size()
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, 
            Globals.HEIGHT / 2 - height / 2 + 164))


        surf = font.render("Start Game", True, pygame.color.Color("red"))
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, 
            Globals.HEIGHT / 2 - height / 2 + 64))

        surf = font.render("adjust visual brightness", True, pygame.color.Color("red"))
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, 
            Globals.HEIGHT / 2 - height / 2 - 36))

        surf = font.render("adjust visual brightness", True, pygame.color.Color("red"))
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, 
            Globals.HEIGHT / 2 - height / 2 - 136))

        surf = font.render("display high-scores", True, pygame.color.Color("red"))
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, 
            Globals.HEIGHT / 2 - height / 2 - 236))

        surf = font.render("quit", True, pygame.color.Color("red"))
        Globals.SCREEN.blit(surf, (Globals.WIDTH / 2 - width / 2, 
            Globals.HEIGHT / 2 - height / 2 - 336))
        pygame.display.flip()

    def update(self, time):
        self.time += time

    def event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if self.selection != 0:
            	self.selection -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if self.selection != 4:
            	self.selection += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.selection == 0:
            	Globals.STATE = MainGame()
            if self.selection == 3:
                # Globals.STATE = Score()
                pass
            if self.selection == 4:
            	sys.exit()