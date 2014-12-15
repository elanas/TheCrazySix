from GameState import GameState
from Globals import Globals
from SettingsManager import SettingsManager
from asset_loader import AssetLoader
import pygame
import Menu
from EventManager import EventManager

PAUSE_IMAGE = pygame.image.load("images/game-paused.png")

class PauseScreen(GameState):
    UNPAUSE_KEYS = [pygame.K_p, pygame.K_RETURN]
    TITLE_FONT = pygame.font.Font(None, 100)
    TITLE_TEXT = 'Game Paused'
    TITLE_COLOR = pygame.color.Color('white')
    ALPHA_FACTOR = 550
    MIN_ALPHA = 0
    MAX_ALPHA = 255

    def __init__(self, return_state, escape_state=None):
        self.return_state = return_state
        self.escape_state = escape_state if escape_state is not None else \
            Menu.Menu()
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        Globals.play_menu_sound()
        self.title_surf = PauseScreen.TITLE_FONT.render(
            PauseScreen.TITLE_TEXT, True, PauseScreen.TITLE_COLOR)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.center = Globals.SCREEN.get_rect().center
        self.black_surf = pygame.Surface(
            (Globals.WIDTH, Globals.HEIGHT)).convert()
        self.black_surf.fill((0, 0, 0))
        self.fade_in = False
        self.fade_out = False
        self.alpha_factor = 300
        self.start_fade_in()

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        # Globals.SCREEN.blit(self.title_surf, self.title_rect)
        Globals.SCREEN.blit(PAUSE_IMAGE, [175, Globals.HEIGHT/3])

        if self.fade_out or self.fade_in:
            Globals.SCREEN.blit(self.black_surf, (0, 0))

    def update(self, time):
        if self.fade_out:
            old_alpha = self.black_surf.get_alpha()
            new_alpha = int(old_alpha + time * PauseScreen.ALPHA_FACTOR)
            if new_alpha >= PauseScreen.MAX_ALPHA:
                self.handle_finish_fade_out()
                self.fade_out = False
            self.black_surf.set_alpha(new_alpha)
        elif self.fade_in:
            old_alpha = self.black_surf.get_alpha()
            new_alpha = int(old_alpha - time * PauseScreen.ALPHA_FACTOR)
            if new_alpha <= PauseScreen.MIN_ALPHA:
                self.fade_in = False
            self.black_surf.set_alpha(new_alpha)

    def start_fade_out(self):
        self.black_surf.set_alpha(PauseScreen.MIN_ALPHA)
        self.fade_out = True

    def start_fade_in(self):
        self.black_surf.set_alpha(PauseScreen.MAX_ALPHA)
        self.fade_in = True

    def handle_finish_fade_out(self):
        fn = getattr(self.return_state, "handle_unpause", None)
        if callable(fn):
            fn()
        Globals.STATE = self.return_state

    def handle_escape(self):
        Globals.STATE = self.escape_state

    def handle_return(self):
        Globals.stop_menu_sound()
        self.start_fade_out()

    def handle_action_key(self):
        Globals.stop_menu_sound()
        self.start_fade_out()

    def handle_raw_event(self, event):
        if EventManager.is_keyboard_event(event.type) and \
                not event in SettingsManager.EVENTS_ESCAPE and \
                not event in SettingsManager.EVENTS_RETURN and \
                not event in SettingsManager.EVENTS_ACTION:
            self.handle_return()
