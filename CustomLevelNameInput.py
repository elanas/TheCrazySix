import pygame
from Globals import Globals
from GameState import GameState
from asset_loader import AssetLoader
import CustomLevelPicker
from LevelEditor.LevelEditor import LevelEditor
from os.path import join
from FileManager import FileManager
import shutil


class CustomLevelNameInput(GameState):
    MIN_LENGTH = 3
    MAX_LENGTH = 15
    PROMPT_FONT = None
    PROMPT_COLOR = (240, 250, 190)
    PROMPT_PADDING = 70
    PROMPT_SIZE = 100
    PROMPT = "Please type the level name"
    INPUT_FONT = None
    INPUT_SIZE = 70
    HIGHLIGHT_PADDING_HEIGHT = 10
    HIGHLIGHT_PADDING_WIDTH = 20
    HIGHLIGHT_COLOR = pygame.color.Color("black")
    HIGHLIGHT_ALPHA = 150
    INPUT_COLOR = pygame.color.Color("white")
    HINT = "Press Enter to continue"
    HINT_FONT = None
    HINT_SIZE = 30
    HINT_PADDING = 400
    HINT_COLOR = pygame.color.Color("white")
    ERROR_FONT = None
    ERROR_SIZE = 40
    ERROR_PADDING = 110
    # ERROR_COLOR = pygame.color.Color("red")
    ERROR_COLOR = (255, 71, 71)
    ERROR_BACKSPACE = "You can't delete nothing!"
    ERROR_TOO_LONG = "Name is too long!"
    ERROR_TOO_SHORT = "Name is too short!"
    ERROR_EXISTS = "A map with that name exists!"
    EXTRA_BLINK_TIME = .75
    EXTRA_POSTTEXT = '|'
    EXTRA_COLOR = pygame.color.Color("white")
    MAP_FILE_EXT = 'txt'
    CUSTOM_MAP_PATH = join('maps', 'custom')
    PLAY_PATH = 'custom'
    BASE_MAP_PATH = join('maps', 'base_custom.txt')

    def __init__(self):
        Globals.INTRO_SOUND_PLAYED = False
        self.file_name = ""
        self.error_message = None
        self.loader = AssetLoader('images')
        self.setup_text()
        self.show_extra = False
        self.extra_time = 0
        Globals.play_menu_sound()
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        self.file_manager = FileManager(
            path=CustomLevelNameInput.CUSTOM_MAP_PATH,
            file_ext=CustomLevelNameInput.MAP_FILE_EXT)

    def setup_text(self):
        self.input_font = pygame.font.Font(CustomLevelNameInput.INPUT_FONT,
                                           CustomLevelNameInput.INPUT_SIZE)
        self.hint_font = pygame.font.Font(
            CustomLevelNameInput.HINT_FONT,
            CustomLevelNameInput.HINT_SIZE
        )
        self.error_font = pygame.font.Font(CustomLevelNameInput.ERROR_FONT,
                                           CustomLevelNameInput.ERROR_SIZE)
        self.prompt_font = pygame.font.Font(CustomLevelNameInput.PROMPT_FONT,
                                            CustomLevelNameInput.PROMPT_SIZE)
        self.prompt_surf = self.prompt_font.render(CustomLevelNameInput.PROMPT, True,
                                                   CustomLevelNameInput.PROMPT_COLOR)

        self.prompt_rect = self.prompt_surf.get_rect()
        self.prompt_rect.centerx = Globals.WIDTH / 2
        self.prompt_rect.top = CustomLevelNameInput.PROMPT_PADDING

        self.hint_surf = self.hint_font.render(
            CustomLevelNameInput.HINT,
            True,
            CustomLevelNameInput.HINT_COLOR
        )
        self.hint_rect = self.hint_surf.get_rect()
        self.hint_rect.centerx = Globals.WIDTH / 2
        self.hint_rect.top = CustomLevelNameInput.HINT_PADDING

    def update(self, time):
        self.extra_time += time
        if self.extra_time >= CustomLevelNameInput.EXTRA_BLINK_TIME:
            self.extra_time = 0
            self.show_extra = not self.show_extra

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.prompt_surf, self.prompt_rect)
        Globals.SCREEN.blit(self.hint_surf, self.hint_rect)

        if self.error_message is not None:
            error_surf = self.error_font.render(self.error_message, True,
                                                CustomLevelNameInput.ERROR_COLOR)
            error_rect = error_surf.get_rect()
            error_rect.centerx = Globals.WIDTH / 2
            error_rect.bottom = Globals.HEIGHT - CustomLevelNameInput.ERROR_PADDING
            Globals.SCREEN.blit(error_surf, error_rect)

        input_rect = None

        if len(self.file_name) > 0:
            input_surf = self.input_font.render(self.file_name, True,
                                                CustomLevelNameInput.INPUT_COLOR)
            input_rect = input_surf.get_rect()
            input_rect.centerx = Globals.WIDTH / 2
            input_rect.centery = Globals.HEIGHT / 2
            highlight_rect = input_rect.inflate(
                CustomLevelNameInput.HIGHLIGHT_PADDING_WIDTH * 2,
                CustomLevelNameInput.HIGHLIGHT_PADDING_HEIGHT * 2)
            highlight_surf = pygame.Surface(highlight_rect.size).convert()
            highlight_surf.fill(CustomLevelNameInput.HIGHLIGHT_COLOR)
            highlight_surf.set_alpha(CustomLevelNameInput.HIGHLIGHT_ALPHA)
            Globals.SCREEN.blit(highlight_surf, highlight_rect)
            Globals.SCREEN.blit(input_surf, input_rect)
        if self.show_extra:
            extra_surf = self.input_font.render(CustomLevelNameInput.EXTRA_POSTTEXT,
                                                True,
                                                CustomLevelNameInput.EXTRA_COLOR)
            extra_rect = extra_surf.get_rect()
            extra_rect.centery = Globals.HEIGHT / 2
            if input_rect is not None:
                extra_rect.left = input_rect.right
            else:
                extra_rect.centerx = Globals.WIDTH / 2
                highlight_rect = extra_rect.inflate(
                    CustomLevelNameInput.HIGHLIGHT_PADDING_WIDTH * 2,
                    CustomLevelNameInput.HIGHLIGHT_PADDING_HEIGHT * 2)
                highlight_surf = pygame.Surface(highlight_rect.size).convert()
                highlight_surf.fill(CustomLevelNameInput.HIGHLIGHT_COLOR)
                highlight_surf.set_alpha(CustomLevelNameInput.HIGHLIGHT_ALPHA)
                Globals.SCREEN.blit(highlight_surf, highlight_rect)
            Globals.SCREEN.blit(extra_surf, extra_rect)

    def handle_entry(self, typed_char):
        if len(self.file_name) == CustomLevelNameInput.MAX_LENGTH:
            self.error_message = CustomLevelNameInput.ERROR_TOO_LONG
        else:
            self.file_name += typed_char

    def handle_backspace(self):
        if len(self.file_name) > 0:
            self.file_name = \
                self.file_name[0:len(self.file_name) - 1]
        else:
            self.error_message = CustomLevelNameInput.ERROR_BACKSPACE

    def handle_return(self):
        if len(self.file_name) < CustomLevelNameInput.MIN_LENGTH:
            self.error_message = CustomLevelNameInput.ERROR_TOO_SHORT
        else:
            if self.file_name in self.file_manager.get_files(strip_ext=True):
                self.error_message = CustomLevelNameInput.ERROR_EXISTS
            else:
                full_name = self.file_manager.fix_ext(self.file_name)
                full_path = join(CustomLevelNameInput.CUSTOM_MAP_PATH, full_name)
                self.create_map_file(full_path)
                Globals.STATE = LevelEditor(join('maps', 'map_def.txt'),
                    join(CustomLevelNameInput.CUSTOM_MAP_PATH, full_name),
                    globals=Globals, in_game=True)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            self.error_message = None
            if event.key == pygame.K_ESCAPE:
                Globals.STATE = CustomLevelPicker.CustomLevelPicker()
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

    def create_map_file(self, file_path):
        shutil.copy(CustomLevelNameInput.BASE_MAP_PATH, file_path)
