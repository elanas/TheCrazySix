import pygame

from GameState import GameState
from Globals import Globals
import Menu

BACKGROUND_IMG = pygame.image.load("images/background.png")

class LoseGame(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0]) 
        font = pygame.font.SysFont(None, 80)

        TITLE_PADDING = 150
        VERT_SPACING = 75

        COLOR = (7, 147, 240)

        score_string = "Lost Game" 
        title_surf = font.render(score_string, True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)

        # score = "Score: " + str(int(Globals.PLAYER_SCORE)) + " pts" 
        score = "Score: 10pts"
        title_surf = font.render(score, True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery = Globals.SCREEN.get_rect().centery
        Globals.SCREEN.blit(title_surf, title_rect)

        font = pygame.font.SysFont(None, 30)
        op1 = "Press escape to see Highscores."
        title_surf = font.render(op1, True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery = Globals.SCREEN.get_rect().centery + VERT_SPACING
        Globals.SCREEN.blit(title_surf, title_rect)

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu.Highscore()
