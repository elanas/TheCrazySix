import pygame
from Globals import Globals
from GameState import GameState
from TileTest import TileTest
from asset_loader import AssetLoader
import Menu

BACKGROUND_IMG = pygame.image.load("images/menu_background.png")

class NameInput(GameState):
    MIN_LENGTH = 3
    MAX_LENGTH = 15
    PROMPT_FONT = None
    PROMPT_COLOR = pygame.color.Color("black")
    PROMPT_PADDING = 70
    PROMPT_SIZE = 100
    PROMPT = "Please type your name"
    INPUT_FONT = None
    INPUT_SIZE = 60
    INPUT_SURF_PADDING = 20
    INPUT_COLOR = pygame.color.Color("black")
    INPUT_BG_COLOR = pygame.color.Color("white")
    ERROR_FONT = None
    ERROR_SIZE = 40
    ERROR_PADDING = 70
    ERROR_COLOR = pygame.color.Color("red")
    ERROR_BACKSPACE = "You can't delete nothing!"
    ERROR_TOO_LONG = "Your name is too long!"
    ERROR_TOO_SHORT = "Your name is too short to continue!"

    def __init__(self):
        if Globals.PLAYER_NAME is None:
            Globals.PLAYER_NAME = ""
        self.error_message = None
        self.loader = AssetLoader('images')
        # self.background_image = self.loader.load_image("titlepage_image.jpg")
        self.setup_text()

    def setup_text(self):
        self.input_font = pygame.font.Font(NameInput.INPUT_FONT,
                                           NameInput.INPUT_SIZE)
        self.error_font = pygame.font.Font(NameInput.ERROR_FONT,
                                           NameInput.ERROR_SIZE)
        self.prompt_font = pygame.font.Font(NameInput.PROMPT_FONT,
                                            NameInput.PROMPT_SIZE)
        self.prompt_surf = self.prompt_font.render(NameInput.PROMPT, True,
                                                   NameInput.PROMPT_COLOR)
        self.prompt_rect = self.prompt_surf.get_rect()
        self.prompt_rect.centerx = Globals.WIDTH / 2
        self.prompt_rect.top = NameInput.PROMPT_PADDING

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0]) 
        Globals.SCREEN.blit(self.prompt_surf, self.prompt_rect)

        if self.error_message is not None:
            error_surf = self.error_font.render(self.error_message, True,
                                                NameInput.ERROR_COLOR)
            error_rect = error_surf.get_rect()
            error_rect.centerx = Globals.WIDTH / 2
            error_rect.bottom = Globals.HEIGHT - NameInput.ERROR_PADDING
            Globals.SCREEN.blit(error_surf, error_rect)

        if len(Globals.PLAYER_NAME) > 0:
            input_surf = self.input_font.render(Globals.PLAYER_NAME, True,
                                                NameInput.INPUT_COLOR)
            input_rect = input_surf.get_rect()
            input_rect.centerx = Globals.WIDTH / 2
            input_rect.centery = Globals.HEIGHT / 2
            input_bg_rect = input_rect.inflate(NameInput.INPUT_SURF_PADDING,
                                               NameInput.INPUT_SURF_PADDING)
            Globals.SCREEN.fill(NameInput.INPUT_BG_COLOR, input_bg_rect)
            Globals.SCREEN.blit(input_surf, input_rect)

    def handle_entry(self, typed_char):
        if len(Globals.PLAYER_NAME) == NameInput.MAX_LENGTH:
            self.error_message = NameInput.ERROR_TOO_LONG
        else:
            Globals.PLAYER_NAME += typed_char

    def handle_backspace(self):
        if len(Globals.PLAYER_NAME) > 0:
            Globals.PLAYER_NAME = \
                Globals.PLAYER_NAME[0:len(Globals.PLAYER_NAME) - 1]
        else:
            self.error_message = NameInput.ERROR_BACKSPACE

    def handle_return(self):
        if len(Globals.PLAYER_NAME) < NameInput.MIN_LENGTH:
            self.error_message = NameInput.ERROR_TOO_SHORT
        else:
            Globals.STATE = TileTest()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            self.error_message = None
            if event.key == pygame.K_ESCAPE:
                Globals.STATE = Menu.Menu()
            elif self.is_valid(event.key):
                self.handle_entry(self.parse_key(event.key))
            elif event.key == pygame.K_BACKSPACE:
                self.handle_backspace()
            elif event.key == pygame.K_RETURN:
                self.handle_return()

    def parse_key(self, event_key):
        if self.is_num(event_key):
            return chr(event_key)
        mods = pygame.key.get_mods()
        shift_pressed = mods & pygame.KMOD_SHIFT
        if shift_pressed:
            if event_key == pygame.K_MINUS:
                return chr(pygame.K_UNDERSCORE)
            else:
                return chr(event_key).upper()
        else:
            return chr(event_key)

    def is_valid(self, event_key):
        return self.is_alpha(event_key) or self.is_num(event_key) or \
            event_key == pygame.K_MINUS

    def is_num(self, event_key):
        return pygame.K_0 <= event_key and event_key <= pygame.K_9

    def is_alpha(self, event_key):
        return pygame.K_a <= event_key and event_key <= pygame.K_z
