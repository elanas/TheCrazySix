import pygame
from asset_loader import AssetLoader


class Syringe (pygame.sprite.Sprite):
	def __init__(self, x, y, left):
		self.x = x
		self.y = y
		self.left = left
		self.image = None
		self.rect = None
		self.loader = AssetLoader("images")

class NormalSyringe(Syringe):
	def __init__(self, x, y, left):
		super(NormalSyringe, self).__init__(x,y,left)
		if left:
			self.image = self.loader.load_image_alpha("normal_syringe_left.png")
			self.rect = None
