import pygame

from GameState import GameState
from Globals import Globals
import NameInput
from IntroScreen import IntroScreen

TITLE_COLOR = pygame.color.Color("white")
TITLE_PADDING = 110
BACKGROUND_IMG = pygame.image.load("images/background.png")
KEYBOARD_IMG = pygame.image.load("images/keyboard.png")
ENEMY_IMG = pygame.image.load("images/zombie_walking_down_profile.png")
STAIR_IMG = pygame.image.load("images/stair_profile.png")
TITLE_IMG = pygame.image.load("images/howtoplay.png")


class HowToPlay(GameState):
    ALT_TITLE = "Press ENTER to continue"
    ALT_FONT = pygame.font.Font(None, 30)
    ALT_COLOR = pygame.color.Color("white")
    ALT_PADDING = 170
    INIT_SIZE = 80
    MAX_DELTA = 8
    TIME_DELTA = .05

    def __init__(self):
        GameState.__init__(self)
        self.size = HowToPlay.INIT_SIZE
        self.delta = 1
        self.time_delta = 0
        self.font = pygame.font.Font(None, self.size)
        # self.title_surf = self.font.render(TITLE, True, TITLE_COLOR)
        # self.title_rect = self.title_surf.get_rect()
        # self.title_rect.centerx = Globals.SCREEN.get_rect().centerx
        # self.title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING

        self.alt_surf = HowToPlay.ALT_FONT.render(HowToPlay.ALT_TITLE, True,
                                                  HowToPlay.ALT_COLOR)
        self.alt_rect = self.alt_surf.get_rect()
        self.alt_rect.centerx = Globals.SCREEN.get_rect().centerx
        self.alt_rect.centery = HowToPlay.MAX_DELTA + \
            HowToPlay.ALT_PADDING

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0])
        Globals.SCREEN.blit(TITLE_IMG, [0, 0])  


        Globals.SCREEN.blit(KEYBOARD_IMG, [50, 300])
        Globals.SCREEN.blit(ENEMY_IMG, [400, 307])
        Globals.SCREEN.blit(STAIR_IMG, [645, 250])

        # title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        # Globals.SCREEN.blit(self.title_surf, self.title_rect)
        Globals.SCREEN.blit(self.alt_surf, self.alt_rect)

    def update(self, time):
        self.time_delta += time

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = NameInput.NameInput()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            Globals.STATE = IntroScreen()
