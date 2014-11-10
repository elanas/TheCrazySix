import pygame

from GameState import GameState
from Globals import Globals
from Menu import Menu

GAME_TITLE = "~Field Day~"
TITLE_COLOR = pygame.color.Color("white")
TITLE_PADDING = 100
BACKGROUND_IMG = pygame.image.load("images/background.png")


class Title(GameState):
    ALT_TITLE = "Press ENTER to continue"
    ALT_FONT = pygame.font.Font(None, 30)
    ALT_COLOR = pygame.color.Color("white")
    ALT_PADDING = 50
    INIT_SIZE = 64
    MAX_DELTA = 8
    TIME_DELTA = .05

    def __init__(self):
        GameState.__init__(self)
        self.size = Title.INIT_SIZE
        self.delta = 1
        self.time_delta = 0
        self.font = pygame.font.Font(None, self.size)
        self.title_surf = self.font.render(GAME_TITLE, True, TITLE_COLOR)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = Globals.SCREEN.get_rect().centerx
        self.title_rect.centery = Globals.SCREEN.get_rect().centery

        self.alt_surf = Title.ALT_FONT.render(Title.ALT_TITLE, True,
                                              Title.ALT_COLOR)
        self.alt_rect = self.alt_surf.get_rect()
        self.alt_rect.centerx = Globals.SCREEN.get_rect().centerx
        self.alt_rect.centery = self.title_rect.bottom + Title.MAX_DELTA + \
            Title.ALT_PADDING
        Globals.play_menu_sound()

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0])
        Globals.SCREEN.blit(self.title_surf, self.title_rect)
        Globals.SCREEN.blit(self.alt_surf, self.alt_rect)

    def update(self, time):
        self.time_delta += time
        if self.time_delta >= Title.TIME_DELTA:
            self.time_delta = 0
            self.size += self.delta
            self.font = pygame.font.Font(None, self.size)
            self.title_surf = self.font.render(GAME_TITLE, True, TITLE_COLOR)
            self.title_rect = self.title_surf.get_rect()
            self.title_rect.centerx = Globals.SCREEN.get_rect().centerx
            self.title_rect.centery = Globals.SCREEN.get_rect().centery
            if self.size >= Title.INIT_SIZE + self.MAX_DELTA or \
                    self.size <= Title.INIT_SIZE - self.MAX_DELTA:
                self.delta *= -1

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            Globals.STATE = Menu()
