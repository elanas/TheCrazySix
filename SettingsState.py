from GameState import GameState
from Globals import Globals
from SettingsManager import SettingsManager
from asset_loader import AssetLoader
from SettingsSlider import SettingsSlider
from ControlSettings import ControlSettings
import Menu
import pygame


class SettingsState(GameState):
    SLIDER_SIZE = (400, 50)
    SLIDER_DELTA = 10
    MIN_BRIGHTNESS = 30
    TITLE_IMAGE_PATH = 'settings.png'
    CONTROL_IMAGE_PATH = 'control_settings_small.png'
    # VOLUME_IMAGE_PATH = 'volume.png'
    TITLE_MARGIN_TOP = 60
    TITLE_MARGIN_BOTTOM = 50
    LABEL_SLIDER_MARGIN = 5
    SLIDER_MARGIN = 50
    LABEL_FONT = pygame.font.Font(None, 60)
    LABEL_COLOR = pygame.color.Color('white')
    VOLUME_LABEL = ''
    VOLUME_IMG = pygame.image.load('images/volume.png')
    BRIGHTNESS_LABEL = 'brightness'

    def __init__(self):
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        self.volume_img = self.loader.load_image('volume.png')
        Globals.play_menu_sound()
        self.title_surf = self.loader.load_image_alpha(
            SettingsState.TITLE_IMAGE_PATH)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = Globals.WIDTH / 2
        self.title_rect.top = SettingsState.TITLE_MARGIN_TOP
        self.control_index = 0
        self.init_labels()
        self.init_sliders()
        self.selected = 0

    def init_labels(self):
        self.volume_label_surf = SettingsState.LABEL_FONT.render(
            SettingsState.VOLUME_LABEL, True, SettingsState.LABEL_COLOR)
        self.volume_label_surf.blit(SettingsState.VOLUME_IMG, self.volume_label_surf.get_rect())
        self.volume_label_rect = self.volume_label_surf.get_rect()
        self.volume_label_rect.centerx = Globals.WIDTH / 2
        self.volume_label_rect.top = self.title_rect.bottom + \
            SettingsState.TITLE_MARGIN_BOTTOM

        self.brightness_label_surf = SettingsState.LABEL_FONT.render(
            SettingsState.BRIGHTNESS_LABEL, True, SettingsState.LABEL_COLOR)
        self.brightness_label_rect = self.brightness_label_surf.get_rect()
        self.brightness_label_rect.centerx = Globals.WIDTH / 2
        self.brightness_label_rect.top = self.volume_label_rect.bottom + \
            SettingsState.LABEL_SLIDER_MARGIN + \
            SettingsState.SLIDER_SIZE[1] + SettingsState.SLIDER_MARGIN

        self.control_surfs = self.loader.load_spritesheet_alpha(
            SettingsState.CONTROL_IMAGE_PATH, num_rows=2, num_cols=1)
        self.control_rect = self.control_surfs[0].get_rect()
        self.control_rect.centerx = Globals.WIDTH / 2
        self.control_rect.top = self.brightness_label_rect.bottom + \
            SettingsState.LABEL_SLIDER_MARGIN + \
            SettingsState.SLIDER_SIZE[1] + SettingsState.SLIDER_MARGIN

    def init_sliders(self):
        volume_slider_rect = pygame.Rect((0, 0), SettingsState.SLIDER_SIZE)
        volume_slider_rect.centerx = Globals.WIDTH / 2
        volume_slider_rect.top = self.volume_label_rect.bottom + \
            SettingsState.LABEL_SLIDER_MARGIN
        self.volume_slider = SettingsSlider(
            volume_slider_rect,
            max_value=100, value=SettingsManager.VOLUME)
        self.volume_slider.select()
        brightness_slider_rect = pygame.Rect((0, 0), SettingsState.SLIDER_SIZE)
        brightness_slider_rect.centerx = Globals.WIDTH / 2
        brightness_slider_rect.top = self.brightness_label_rect.bottom + \
            SettingsState.LABEL_SLIDER_MARGIN
        self.brightness_slider = SettingsSlider(
            brightness_slider_rect,
            max_value=(100 - SettingsState.MIN_BRIGHTNESS),
            value=(SettingsManager.BRIGHTNESS - SettingsState.MIN_BRIGHTNESS))

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.title_surf, self.title_rect)
        Globals.SCREEN.blit(self.volume_label_surf, self.volume_label_rect)

        Globals.SCREEN.blit(self.brightness_label_surf,
                            self.brightness_label_rect)
        Globals.SCREEN.blit(self.control_surfs[self.control_index],
                            self.control_rect)
        self.volume_slider.render(Globals.SCREEN)
        self.brightness_slider.render(Globals.SCREEN)

    def update(self, time):
        self.volume_slider.update(time)
        self.brightness_slider.update(time)

    def change_selection(self, delta):
        self.selected = (self.selected + delta) % 3
        if self.selected == 0:
            self.control_index = 0
            self.volume_slider.select()
            self.brightness_slider.deselect()
        if self.selected == 1:
            self.control_index = 0
            self.volume_slider.deselect()
            self.brightness_slider.select()
        elif self.selected == 2:
            self.control_index = 1
            self.brightness_slider.deselect()
            self.volume_slider.deselect()

    def change_value(self, factor=1):
        if self.selected == 0:
            self.volume_slider.change_value(
                SettingsState.SLIDER_DELTA * factor)
            Globals.set_volume(self.volume_slider.value)
        elif self.selected == 1:
            self.brightness_slider.change_value(
                SettingsState.SLIDER_DELTA * factor)
            Globals.set_brightness(SettingsState.MIN_BRIGHTNESS + \
                                   self.brightness_slider.value)

    def handle_escape(self):
        Globals.STATE = Menu.Menu()

    def handle_return(self):
        if self.selected == 2:
            Globals.STATE = ControlSettings()

    def handle_key_left(self, keydown):
        if keydown:
            self.change_value(-1)

    def handle_key_right(self, keydown):
        if keydown:
            self.change_value(1)

    def handle_key_up(self, keydown):
        if keydown:
            self.change_selection(-1)

    def handle_key_down(self, keydown):
        if keydown:
            self.change_selection(1)
