import pygame

from GameState import GameState
from Globals import Globals
import Menu

BACKGROUND_IMG = pygame.image.load("images/menu_background.png")

class WinGame(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0]) 
        font = pygame.font.SysFont("hannotatesc", 64)
        # font.
        TITLE_PADDING = 75
        VERT_SPACING = 75

        COLOR = (7, 147, 240)
        score_string = "You finished the level! You scored " + str(Globals.PLAYER_SCORE) + " points." 
        title_surf = font.render(score_string, True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx - 120
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)

        op1 = font.render("Press escape to see Highscores.", True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op1, title_rect)
        pygame.display.flip()

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu.Highscore()
