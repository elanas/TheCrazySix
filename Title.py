import pygame

from GameState import GameState
from Globals import Globals
import Menu

GAME_TITLE = "~Field Day~"
TITLE_COLOR = pygame.color.Color("white")
TITLE_PADDING = 100
BACKGROUND_IMG = pygame.image.load("images/background.png")
IMG = pygame.image.load("images/settings.png")


class Title(GameState):
    ALT_TITLE = "Press ENTER to continue"
    ALT_FONT = pygame.font.Font(None, 30)
    ALT_COLOR = pygame.color.Color("white")
    MAX_DELTA = 20
    ALT_PADDING = 50
    TIME_DELTA = .05

    def __init__(self):
        GameState.__init__(self)
        # self.size = Title.INIT_SIZE
        self.diff = 0
        self.delta = 1
        self.time_delta = 0
        # self.font = pygame.font.Font(None, self.size)
        # self.base_surf = self.font.render(GAME_TITLE, True, TITLE_COLOR)
        self.base_surf = IMG
        self.base_size = self.base_surf.get_rect().size
        # Title.INIT_SIZE = self.base_size[1]
        self.widthrat = self.base_size[0] / self.base_size[1]
        self.title_surf = self.base_surf
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
            orig_h = self.base_surf.get_rect().height
            orig_w = self.base_surf.get_rect().width
            self.time_delta = 0
            self.diff += self.delta
            self.title_surf = pygame.transform.smoothscale(
                self.base_surf,
                (self.base_size[0] + self.diff * (orig_w / orig_h),
                 self.base_size[1] + self.diff))
            self.old_rect = self.title_rect
            self.title_rect = self.title_surf.get_rect()
            self.title_rect.center = self.old_rect.center
            
            if self.title_rect.height >= orig_h + self.MAX_DELTA or \
                    self.title_rect.height <= orig_h - self.MAX_DELTA:
                self.delta *= -1

    def handle_return(self):
        Globals.STATE = Menu.Menu()

    def handle_escape(self):
        self.handle_quit()
