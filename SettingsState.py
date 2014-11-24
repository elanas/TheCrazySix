from GameState import GameState
from Globals import Globals
from asset_loader import AssetLoader
import Menu
import pygame


class SettingsState(GameState):
	TEMP_FONT = pygame.font.Font(None, 150)
	TEMP_COLOR = (240, 250, 190)

	def __init__(self):
		self.loader = AssetLoader('images')
		self.background_img = self.loader.load_image('background.png')
		Globals.play_menu_sound()
		self.temp_surf = SettingsState.TEMP_FONT.render(
			'Coming Soon', True, SettingsState.TEMP_COLOR)
		self.temp_rect = self.temp_surf.get_rect()
		self.temp_rect.center = Globals.SCREEN.get_rect().center

	def render(self):
		Globals.SCREEN.blit(self.background_img, (0, 0))
		Globals.SCREEN.blit(self.temp_surf, self.temp_rect)

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				Globals.STATE = Menu.Menu()