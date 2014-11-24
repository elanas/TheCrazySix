from GameState import GameState
from Globals import Globals
from asset_loader import AssetLoader
import pygame
import Menu


class PauseScreen(GameState):
    UNPAUSE_KEYS = [pygame.K_p, pygame.K_RETURN]
    TITLE_FONT = pygame.font.Font(None, 100)
    TITLE_TEXT = 'Game Paused'
    TITLE_COLOR = pygame.color.Color('white')

    def __init__(self, return_state):
        self.return_state = return_state
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        Globals.play_menu_sound()
        self.title_surf = PauseScreen.TITLE_FONT.render(
            PauseScreen.TITLE_TEXT, True, PauseScreen.TITLE_COLOR)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.center = Globals.SCREEN.get_rect().center


    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.title_surf, self.title_rect)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_ESCAPE:
                Globals.STATE = Menu.Menu()
            if key in PauseScreen.UNPAUSE_KEYS:
                Globals.stop_menu_sound()
                self.return_state.handle_unpause()
                Globals.STATE = self.return_state
