import pygame

from GameState import GameState
from Globals import Globals
from HighscoreManager import HighscoreManager
import Menu

BACKGROUND_IMG = pygame.image.load("images/background.png")
TITLE_IMG = pygame.image.load("images/highscore.png")


class Highscore(GameState):
    HIGHSCORE_BACKGROUND = pygame.color.Color("black")
    HIGHSCORE_ALPHA = 150
    HIGHSCORE_PADDING = 5

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0.0
        self.highscoreManager = HighscoreManager()

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0])
        Globals.SCREEN.blit(TITLE_IMG, [Globals.WIDTH / 5.5, 0])
        font = pygame.font.SysFont(None, 64)

        TITLE_PADDING = 100
        VERT_SPACING = 90
        TOP_SPACE = 100

        COLOR = (255, 255, 255)

        highscore_rect = pygame.Rect(0, 0, Globals.WIDTH/2, Globals.HEIGHT/2 + 100)
        highscore_rect.centerx = Globals.WIDTH/2
        highscore_rect.centery = Globals.HEIGHT/2 + 50
        highscore_surf = pygame.Surface(highscore_rect.size).convert()
        highscore_surf.fill(Highscore.HIGHSCORE_BACKGROUND)
        highscore_surf.set_alpha(Highscore.HIGHSCORE_ALPHA)
        Globals.SCREEN.blit(highscore_surf, highscore_rect)


        highscoreEntry = self.highscoreManager.get_list()

        op1 = font.render("{} - {}".format(
            highscoreEntry[0].name,
            highscoreEntry[0].score
        ), True, COLOR)
        title_rect = op1.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery += TOP_SPACE + VERT_SPACING
        Globals.SCREEN.blit(op1, title_rect)

        op2 = font.render("{} - {}".format(
            highscoreEntry[1].name,
            highscoreEntry[1].score
        ), True, COLOR)
        title_rect = op2.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery += TOP_SPACE + (2 * VERT_SPACING)
        Globals.SCREEN.blit(op2, title_rect)

        op3 = font.render("{} - {}".format(
            highscoreEntry[2].name,
            highscoreEntry[2].score
        ), True, COLOR)
        title_rect = op3.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery += TOP_SPACE + (3 * VERT_SPACING)
        Globals.SCREEN.blit(op3, title_rect)

        op4 = font.render("{} - {}".format(
            highscoreEntry[3].name,
            highscoreEntry[3].score
        ), True, COLOR)
        title_rect = op4.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery += TOP_SPACE + (4 * VERT_SPACING)
        Globals.SCREEN.blit(op4, title_rect)

    def update(self, time):
        pass

    def handle_escape(self):
        Globals.STATE = Menu.Menu()
