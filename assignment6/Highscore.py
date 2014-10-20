import pygame

from GameState import GameState
from Globals import Globals
from HighscoreManager import HighscoreManager
import Menu

BACKGROUND_IMG = pygame.image.load("images/titlepage_image.jpg")


class Highscore(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0.0

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0]) 
        font = pygame.font.SysFont(None, 64)

        TITLE_PADDING = 100
        VERT_SPACING = 90

        COLOR = (7, 147, 240)

        title_surf = font.render("Highscores", True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)
        highscoreManager = HighscoreManager()
        highscoreEntry = highscoreManager.get_list()

        op1 = font.render("{} - {}".format(highscoreEntry[0].name, highscoreEntry[0].score), True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op1, title_rect)

        op2 = font.render("{} - {}".format(highscoreEntry[1].name, highscoreEntry[1].score), True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op2, title_rect)

        op3 = font.render("{} - {}".format(highscoreEntry[2].name, highscoreEntry[2].score), True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op3, title_rect)

        op4 = font.render("{} - {}".format(highscoreEntry[3].name, highscoreEntry[3].score), True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op4, title_rect)

    def update(self, time):
        pass
    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu.Menu()
