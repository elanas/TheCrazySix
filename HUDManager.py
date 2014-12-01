import pygame
from asset_loader import AssetLoader
from Globals import Globals


class HUDManager(object):
	KEY_IMAGE_PATH = 'key.png'
	SPECIAL_KEY_IMAGE_PATH = 'special_key.png'
	MARGIN_BOTTOM = 10
	MARGIN_RIGHT = 10
	PADDING_NEXT = 5
	
	def __init__(self):
		self.num_keys = 0
		self.num_special_keys = 0
		self.loader = AssetLoader('images')
		self.init_images()
		self.update_surface()

	def init_images(self):
		self.key_surf = self.loader.load_image_alpha(HUDManager.KEY_IMAGE_PATH)
		self.key_rect = self.key_surf.get_rect()
		self.special_key_surf = self.loader.load_image_alpha(
			HUDManager.SPECIAL_KEY_IMAGE_PATH)
		self.special_key_rect = self.special_key_surf.get_rect()
		# assuming images are the same size
		self.image_width = self.key_rect.width
		self.image_height = self.key_rect.height

	def update_surface(self):
		num_obj = self.num_keys + self.num_special_keys
		surf_width = num_obj * (self.image_width + HUDManager.PADDING_NEXT)
		surf_height = self.image_height
		self.surface = pygame.Surface((surf_width, surf_height), 
									  pygame.SRCALPHA, 32).convert_alpha()
		self.rect = self.surface.get_rect()
		self.rect.bottom = Globals.HEIGHT - HUDManager.MARGIN_BOTTOM
		self.rect.right = Globals.WIDTH - HUDManager.MARGIN_RIGHT
		self.blit_images()

	def blit_images(self):
		curr_x = self.rect.width - self.image_width
		for i in range(0, self.num_keys):
			self.surface.blit(self.key_surf, (curr_x, 0))
			curr_x -= self.image_width + HUDManager.PADDING_NEXT

		for i in range(0, self.num_special_keys):
			self.surface.blit(self.special_key_surf, (curr_x, 0))
			curr_x -= self.image_width + HUDManager.PADDING_NEXT

	def render(self, screen):
		self.blit_images()
		screen.blit(self.surface, self.rect)

	def add_key(self):
		self.num_keys += 1
		self.update_surface()

	def add_special_key(self):
		self.num_special_keys += 1
		self.update_surface()

	def has_key(self):
		return self.num_keys > 0

	def has_special_key(self):
		return self.num_special_keys > 0

	def use_key(self):
		if self.has_key():
			self.num_keys -= 1
			self.update_surface()
			return True
		return False

	def use_special_key(self):
		if self.has_special_key():
			self.num_special_keys -= 1
			self.update_surface()
			return True
		return False