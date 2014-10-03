import pygame
from Globals import Globals


class Camera(object):

	def __init__(self, tileEngine, container):
		self.tileEngine = tileEngine
		self.container = container
		self.viewpoint = container.copy()


	def render(self, screen):
		curr_y = self.viewpoint.top
		while curr_y - self.viewpoint.top < self.container.bottom:
			curr_x = self.viewpoint.left
			tile_rect = None
			while curr_x - self.viewpoint.left< self.container.right:
				curr_tile = self.tileEngine.get_tile_image(curr_x, curr_y)
				tile_rect = curr_tile.get_rect()
				area = pygame.Rect(curr_x - self.viewpoint.left, curr_y - self.viewpoint.top, tile_rect.width, tile_rect.height)
				screen.blit(curr_tile, area)
				curr_x += tile_rect.width
			curr_y += tile_rect.height

	def move(self, xDelta, yDelta):
		self.viewpoint.x += xDelta
		self.viewpoint.y += yDelta
