from GameState import GameState
from asset_loader import AssetLoader
from Globals import Globals
from os.path import join
from FileManager import FileManager
import pygame
import sys, os
from LevelEditor.LevelEditor import LevelEditor


class CustomLevelPicker(GameState):
    MAP_FILE_EXT = 'txt'
    CUSTOM_MAP_PATH = join('maps', 'custom')
    SELECTION_FONT = pygame.font.Font(None, 70)
    SELECTION_COLOR = pygame.color.Color('white')
    CREATE_NEW_TEXT = 'Create New Level'
    SELECTION_TOP_MARGIN = 30
    SELECTION_PADDING = 20
    HIGHLIGHT_PADDING_HEIGHT = 30
    HIGHLIGHT_PADDING_WIDTH = 70
    HIGHLIGHT_COLOR = pygame.color.Color("black")
    HIGHLIGHT_ALPHA = 150
    ARROW_MARGIN = 20
    
    def __init__(self):
        self.init_images()
        self.file_manager = FileManager(
            path=CustomLevelPicker.CUSTOM_MAP_PATH,
            file_ext=CustomLevelPicker.MAP_FILE_EXT)
        self.file_names = self.file_manager.get_files(strip_ext=True)
        self.current_selection = 0
        self.text_surf = None
        self.text_rect = None
        self.highlight_surf = None
        self.highlight_rect = None
        self.build_text()

    def init_images(self):
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        self.arrow_down_surf = self.loader.load_image_alpha('arrow_down.png')
        self.arrow_down_rect = self.arrow_down_surf.get_rect()
        self.arrow_up_surf = self.loader.load_image_alpha('arrow_up.png')
        self.arrow_up_rect = self.arrow_up_surf.get_rect()
        self.arrow_up_rect.centerx = Globals.WIDTH / 2
        self.arrow_down_rect.centerx = Globals.WIDTH / 2

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.highlight_surf, self.highlight_rect)
        Globals.SCREEN.blit(self.text_surf, self.text_rect)
        Globals.SCREEN.blit(self.arrow_down_surf, self.arrow_down_rect)
        Globals.SCREEN.blit(self.arrow_up_surf, self.arrow_up_rect)

    def build_text(self):
        self.text_surf = CustomLevelPicker.SELECTION_FONT.render(
            self.get_selection_name(), True, CustomLevelPicker.SELECTION_COLOR)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = Globals.SCREEN.get_rect().center
        self.text_rect.top += CustomLevelPicker.SELECTION_TOP_MARGIN
        self.highlight_rect = self.text_rect.inflate(
            CustomLevelPicker.HIGHLIGHT_PADDING_WIDTH,
            CustomLevelPicker.HIGHLIGHT_PADDING_HEIGHT)
        self.highlight_surf = pygame.Surface(self.highlight_rect.size)
        self.highlight_surf.fill(CustomLevelPicker.HIGHLIGHT_COLOR)
        self.highlight_surf.set_alpha(CustomLevelPicker.HIGHLIGHT_ALPHA)
        self.arrow_up_rect.bottom = self.highlight_rect.top - \
            CustomLevelPicker.ARROW_MARGIN
        self.arrow_down_rect.top = self.highlight_rect.bottom + \
            CustomLevelPicker.ARROW_MARGIN

    def get_selection_name(self):
        if self.current_selection == 0:
            return CustomLevelPicker.CREATE_NEW_TEXT
        else:
            return self.file_names[self.current_selection - 1]

    def handle_change(self, delta):
        self.current_selection = (self.current_selection + delta) % \
            (len(self.file_names) + 1)
        self.build_text()

    def handle_selection(self):
        pass

    def handle_edit_selection(self):
        if self.current_selection != 0:
            file_path = self.file_manager.fix_ext(
                self.file_names[self.current_selection - 1])
            Globals.STATE = LevelEditor(join('maps', 'map_def.txt'),
                join(CustomLevelPicker.CUSTOM_MAP_PATH, file_path),
                globals=Globals)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.handle_change(1)
            elif event.key == pygame.K_DOWN:
                self.handle_change(-1)
            elif event.key == pygame.K_RETURN:
                self.handle_selection()
            elif event.key == pygame.K_e:
                self.handle_edit_selection()
            elif event.key == pygame.K_ESCAPE:
                Globals.RUNNING = False
