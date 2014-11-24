from GameState import GameState
from Globals import Globals
from asset_loader import AssetLoader
from SettingsSlider import SettingsSlider
import Menu
import pygame


class SettingsState(GameState):
    SLIDER_SIZE = (400, 50)
    SLIDER_DELTA = .1
    MIN_BRIGHTNESS = .3
    TITLE_IMAGE_PATH = 'settings.png'
    TITLE_MARGIN_TOP = 70
    TITLE_MARGIN_BOTTOM = 80
    LABEL_SLIDER_MARGIN = 5
    SLIDER_MARGIN = 75
    LABEL_FONT = pygame.font.Font(None, 60)
    LABEL_COLOR = pygame.color.Color('white')
    VOLUME_LABEL = 'Volume'
    BRIGHTNESS_LABEL = 'Brightness'

    def __init__(self):
        self.loader = AssetLoader('images')
        self.background_img = self.loader.load_image('background.png')
        Globals.play_menu_sound()
        self.title_surf = self.loader.load_image_alpha(
        	SettingsState.TITLE_IMAGE_PATH)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = Globals.WIDTH / 2
        self.title_rect.top = SettingsState.TITLE_MARGIN_TOP
        self.init_labels()
        self.init_sliders()
        self.selected = 0

    def init_labels(self):
    	self.volume_label_surf = SettingsState.LABEL_FONT.render(
    		SettingsState.VOLUME_LABEL, True, SettingsState.LABEL_COLOR)
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

    def init_sliders(self):
    	volume_slider_rect = pygame.Rect((0, 0), SettingsState.SLIDER_SIZE)
    	volume_slider_rect.centerx = Globals.WIDTH / 2
    	volume_slider_rect.top = self.volume_label_rect.bottom + \
    		SettingsState.LABEL_SLIDER_MARGIN
    	self.volume_slider = SettingsSlider(
    		volume_slider_rect,
    		max_value=1, value=Globals.VOLUME)
    	self.volume_slider.select()
    	brightness_slider_rect = pygame.Rect((0, 0), SettingsState.SLIDER_SIZE)
    	brightness_slider_rect.centerx = Globals.WIDTH / 2
    	brightness_slider_rect.top = self.brightness_label_rect.bottom + \
    		SettingsState.LABEL_SLIDER_MARGIN
    	self.brightness_slider = SettingsSlider(
    		brightness_slider_rect,
    		max_value=(1 - SettingsState.MIN_BRIGHTNESS),
    		value=(Globals.BRIGHTNESS - SettingsState.MIN_BRIGHTNESS))

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.title_surf, self.title_rect)
        Globals.SCREEN.blit(self.volume_label_surf, self.volume_label_rect)
        Globals.SCREEN.blit(self.brightness_label_surf,
        					self.brightness_label_rect)
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
    		Globals.set_volume(self.volume_slider.value)
    	else:
    		self.brightness_slider.change_value(
    			SettingsState.SLIDER_DELTA * factor)
    		Globals.set_brightness(SettingsState.MIN_BRIGHTNESS + \
    							   self.brightness_slider.value)

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
