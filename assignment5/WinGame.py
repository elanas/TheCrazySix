import pygame

from GameState import GameState
from Globals import Globals


class WinGame(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        # font.
        TITLE_PADDING = 75
        VERT_SPACING = 75

        COLOR = (7, 147, 240)

        title_surf = font.render("You finished the level!"
            + "\n Press Escape to return to the menu.", True, (0, 0, 0))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)

        pygame.display.flip()        

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu()

from Menu import Menu
