import pygame

from GameState import GameState
from Globals import Globals
import NameInput

TITLE_COLOR = pygame.color.Color("white")
TITLE_PADDING = 110
BACKGROUND_IMG = pygame.image.load("images/background.png")
KEYBOARD_IMG = pygame.image.load("images/keyboard.png")
ENEMY_IMG = pygame.image.load("images/zombie_walking_down_profile.png")
STAIR_IMG = pygame.image.load("images/stair_profile.png")
TITLE_IMG = pygame.image.load("images/howtoplay.png")
SPACEBAR_IMG = pygame.image.load("images/spacebar.png")
ATTACK_IMG = pygame.image.load("images/attack_key.png")
SUBTITLE_BACKGROUND = pygame.color.Color("black")
SUBTITLE_PADDING = 5
SUBTITLE_TEXT = "Press enter to continue"
SUBTITLE_COLOR = pygame.color.Color("white")
SUBTITLE_FONT = pygame.font.Font(None, 32)
SUBTITLE_MARGIN = 380


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
        self.alpha_factor = 300

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

        self.init_subtitle()
        Globals.play_menu_sound()

    def init_subtitle(self):
        text_surf = SUBTITLE_FONT.render(
            SUBTITLE_TEXT, True, SUBTITLE_COLOR)
        self.subtitle_rect = text_surf.get_rect()
        self.subtitle_rect.centerx = Globals.WIDTH / 2
        self.subtitle_rect.bottom = \
            Globals.HEIGHT - SUBTITLE_MARGIN
        self.subtitle_rect.inflate_ip(
            SUBTITLE_PADDING * 2,
            SUBTITLE_PADDING * 2
        )
        self.subtitle_surf = pygame.Surface(self.subtitle_rect.size).convert()
        self.subtitle_surf.fill(SUBTITLE_BACKGROUND)
        self.subtitle_surf.blit(text_surf, (
            SUBTITLE_PADDING,
            SUBTITLE_PADDING
        ))
        self.subtitle_surf.set_alpha(255)

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0])
        Globals.SCREEN.blit(TITLE_IMG, [0, 0])
        Globals.SCREEN.blit(KEYBOARD_IMG, [0, 300])
        Globals.SCREEN.blit(SPACEBAR_IMG, [400, 307])
        Globals.SCREEN.blit(ATTACK_IMG, [400, 437])
        Globals.SCREEN.blit(STAIR_IMG, [645, 250])
        # Globals.SCREEN.blit(SPACEBAR_IMG, [645, 250])

        # title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        # Globals.SCREEN.blit(self.title_surf, self.title_rect)
        # Globals.SCREEN.blit(self.alt_surf, self.alt_rect)
        Globals.SCREEN.blit(self.subtitle_surf, self.subtitle_rect)

    def update(self, time):
        self.time_delta += time

        old_alpha = self.subtitle_surf.get_alpha()
        if old_alpha == 0 or old_alpha == 255:
            self.alpha_factor *= -1
        new_alpha = int(old_alpha + self.alpha_factor * time)
        if new_alpha < 0:
            new_alpha = 0
        elif new_alpha > 255:
            new_alpha = 255
        self.subtitle_surf.set_alpha(new_alpha)

    def handle_escape(self):
        Globals.STATE = NameInput.NameInput()

    def handle_return(self):
        Globals.reset_game()
        Globals.goto_first_level()
