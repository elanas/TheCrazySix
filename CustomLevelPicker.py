from GameState import GameState
from asset_loader import AssetLoader
from Globals import Globals
from os.path import join
from FileManager import FileManager
import pygame
import sys, os
from LevelEditor.LevelEditor import LevelEditor
from Levels.CustomLevel import CustomLevel


class CustomLevelPicker(GameState):
    MAP_FILE_EXT = 'txt'
    CUSTOM_MAP_PATH = join('maps', 'custom')
    PLAY_PATH = 'custom'
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
    SUBTITLE_BACKGROUND = pygame.color.Color("black")
    SUBTITLE_PADDING = 10
    RIGHT_SUBTITLE_TEXT = "Press enter to play"
    LEFT_SUBTITLE_TEXT = "Press e to edit"
    NEW_SUBTITLE_TEXT = "Press enter"
    SUBTITLE_COLOR = pygame.color.Color("white")
    SUBTITLE_FONT = pygame.font.Font(None, 32)
    SUBTITLE_MARGIN_BOTTOM = 50
    
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
        self.build_subtitles()

    def init_images(self):
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        self.arrow_down_surf = self.loader.load_image_alpha('arrow_down.png')
        self.arrow_down_rect = self.arrow_down_surf.get_rect()
        self.arrow_up_surf = self.loader.load_image_alpha('arrow_up.png')
        self.arrow_up_rect = self.arrow_up_surf.get_rect()
        self.arrow_up_rect.centerx = Globals.WIDTH / 2
        self.arrow_down_rect.centerx = Globals.WIDTH / 2

    def build_subtitles(self):
        self.left_subtitle_surf, self.left_subtitle_rect = self.init_subtitle(
            CustomLevelPicker.LEFT_SUBTITLE_TEXT, Globals.WIDTH / 4)
        self.right_subtitle_surf, self.right_subtitle_rect = \
            self.init_subtitle(CustomLevelPicker.RIGHT_SUBTITLE_TEXT,
                (3 * Globals.WIDTH) / 4)
        self.new_subtitle_surf, self.new_subtitle_rect = \
            self.init_subtitle(CustomLevelPicker.NEW_SUBTITLE_TEXT,
                Globals.WIDTH / 2)

    def init_subtitle(self, text, centerx):
        text_surf = CustomLevelPicker.SUBTITLE_FONT.render(
            text, True, CustomLevelPicker.SUBTITLE_COLOR)
        subtitle_rect = text_surf.get_rect()
        subtitle_rect.bottom = \
            Globals.HEIGHT - CustomLevelPicker.SUBTITLE_MARGIN_BOTTOM
        subtitle_rect.centerx = centerx
        subtitle_rect.inflate_ip(
            CustomLevelPicker.SUBTITLE_PADDING * 2,
            CustomLevelPicker.SUBTITLE_PADDING * 2
        )
        subtitle_surf = pygame.Surface(subtitle_rect.size).convert()
        subtitle_surf.fill(CustomLevelPicker.SUBTITLE_BACKGROUND)
        subtitle_surf.blit(text_surf, (
            CustomLevelPicker.SUBTITLE_PADDING,
            CustomLevelPicker.SUBTITLE_PADDING
        ))
        return subtitle_surf, subtitle_rect

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.highlight_surf, self.highlight_rect)
        Globals.SCREEN.blit(self.text_surf, self.text_rect)
        if self.current_selection == 0:
            Globals.SCREEN.blit(self.new_subtitle_surf, self.new_subtitle_rect)
        else:
            Globals.SCREEN.blit(self.left_subtitle_surf, self.left_subtitle_rect)
            Globals.SCREEN.blit(self.right_subtitle_surf, self.right_subtitle_rect)
        if len(self.file_names) > 0:
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
        if self.current_selection != 0:
            file_path = self.file_manager.fix_ext(
                self.file_names[self.current_selection - 1])
            level = CustomLevel(join(CustomLevelPicker.PLAY_PATH,
                file_path))
            level.got_current_state()
            Globals.STATE = level
        else:
            pass

    def handle_edit_selection(self):
        if self.current_selection != 0:
            file_path = self.file_manager.fix_ext(
                self.file_names[self.current_selection - 1])
            Globals.STATE = LevelEditor(join('maps', 'map_def.txt'),
                join(CustomLevelPicker.CUSTOM_MAP_PATH, file_path),
                globals=Globals)
        else:
            pass

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
