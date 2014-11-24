from GameState import GameState
from Globals import Globals
from asset_loader import AssetLoader
from SettingsSlider import SettingsSlider
import Menu
import pygame


class SettingsState(GameState):
    TEMP_FONT = pygame.font.Font(None, 70)
    TEMP_COLOR = (240, 250, 190)
    TITLE_MARGIN_TOP = 70
    SLIDER_SIZE = (400, 50)
    SLIDER_DELTA = .1

    def __init__(self):
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        Globals.play_menu_sound()
        self.temp_surf = SettingsState.TEMP_FONT.render(
            'Settings', True, SettingsState.TEMP_COLOR)
        self.temp_rect = self.temp_surf.get_rect()
        self.temp_rect.centerx = Globals.WIDTH / 2
        self.temp_rect.top = SettingsState.TITLE_MARGIN_TOP
        self.init_sliders()
        self.selected = 0

    def init_sliders(self):
    	volume_slider_rect = pygame.Rect((0, 0), SettingsState.SLIDER_SIZE)
    	volume_slider_rect.center = Globals.SCREEN.get_rect().center
    	self.volume_slider = SettingsSlider(
    		volume_slider_rect,
    		max_value=1, value=Globals.VOLUME)
    	self.volume_slider.select()
    	brightness_slider_rect = pygame.Rect((0, 0), SettingsState.SLIDER_SIZE)
    	brightness_slider_rect.center = Globals.SCREEN.get_rect().center
    	brightness_slider_rect.top = volume_slider_rect.bottom + 20
    	self.brightness_slider = SettingsSlider(
    		brightness_slider_rect,
    		max_value=1, value=Globals.BRIGHTNESS)

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.temp_surf, self.temp_rect)
        self.volume_slider.render(Globals.SCREEN)
        self.brightness_slider.render(Globals.SCREEN)

    def change_selection(self, delta):
    	self.selected = (self.selected + delta) % 2
    	if self.selected == 0:
    		self.volume_slider.select()
    		self.brightness_slider.deselect()
    	else:
    		self.volume_slider.deselect()
    		self.brightness_slider.select()

    def change_value(self, factor=1):
    	if self.selected == 0:
    		self.volume_slider.change_value(
    			SettingsState.SLIDER_DELTA * factor)
    	else:
    		self.brightness_slider.change_value(
    			SettingsState.SLIDER_DELTA * factor)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                Globals.STATE = Menu.Menu()
            elif event.key == pygame.K_LEFT:
            	self.change_value(-1)
            elif event.key == pygame.K_RIGHT:
            	self.change_value(1)
            elif event.key == pygame.K_UP:
            	self.change_selection(-1)
            elif event.key == pygame.K_DOWN:
            	self.change_selection(1)
