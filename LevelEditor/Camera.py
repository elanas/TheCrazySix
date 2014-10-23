import pygame
from Globals import Globals
from collections import namedtuple


class Camera(object):
    BORDER_COLOR = (0, 0, 0)
    BOTTOM_PADDING = 0
    EMPTY_COLOR = (0, 0, 0)
    TileRectPair = namedtuple('TileRectPair', 'tile rect')

    def __init__(self, tileEngine, container):
        self.tileEngine = tileEngine
        self.container = container
        self.viewpoint = container.copy()
        self.initView()

    def initView(self):
        tileRect = self.tileEngine.get_tile_rect()
        numRows = self.tileEngine.getNumRows()
        # self.viewpoint.top = -17
        # self.viewpoint.left = 11
        # self.viewpoint.bottom = tileRect.height * numRows + \
            # Camera.BOTTOM_PADDING
        # self.viewpoint.centerx = (tileRect.width *
                                  # self.tileEngine.getMaxCols()) / 2

    def render(self, screen, clear_screen=True):
        if clear_screen:
            screen.fill(Camera.EMPTY_COLOR, self.container)
        curr_y = self.viewpoint.top
        while curr_y - self.viewpoint.top + self.container.top < \
                self.container.bottom:
            curr_x = self.viewpoint.left
            while curr_x - self.viewpoint.left + self.container.left < \
                    self.container.right:
                curr_tile_img, curr_rect = \
                    self.tileEngine.get_tile_image(curr_x, curr_y)
                curr_rect.left = \
                    (curr_x - self.viewpoint.left) + self.container.left
                curr_rect.top = \
                    (curr_y - self.viewpoint.top) + self.container.top
                if curr_tile_img is not None:
                    img_area = curr_tile_img.get_rect()
                    if curr_rect.bottom > self.container.bottom:
                        img_area.height -= \
                            curr_rect.bottom - self.container.bottom
                    if curr_rect.right > self.container.right:
                        img_area.width -= \
                            curr_rect.right - self.container.right

                    screen.blit(curr_tile_img, curr_rect, img_area)
                pygame.draw.rect(screen, Camera.BORDER_COLOR, curr_rect, 1)
                curr_x += curr_rect.width
            curr_y += curr_rect.height

    def move(self, xDelta, yDelta):
        self.viewpoint.x += xDelta
        self.viewpoint.y += yDelta

    def get_nearby_tiles(self, center, radius):
        tiles = list()
        curr_y = center[1] - radius
        max_x = center[0] + radius
        max_y = center[1] + radius
        while curr_y < max_y:
            curr_x = center[0] - radius
            trans_y = curr_y + self.viewpoint.top
            while curr_x < max_x:
                trans_x = curr_x + self.viewpoint.left
                curr_tile, curr_rect = \
                    self.tileEngine.get_tile(trans_x, trans_y)
                curr_rect.x = \
                    (curr_rect.x - self.viewpoint.left) + self.container.left
                curr_rect.y = \
                    (curr_rect.y - self.viewpoint.top) + self.container.top
                if curr_rect.bottom > max_y:
                    curr_rect.height -= curr_rect.bottom - max_y
                if curr_rect.right > max_x:
                    curr_rect.width -= curr_rect.right - max_x
                tiles.append(
                    Camera.TileRectPair(tile=curr_tile, rect=curr_rect))
                curr_x += curr_rect.width
            curr_y += curr_rect.height
        return tiles

    def get_solid_tiles(self, center, radius):
        nearby_tiles = self.get_nearby_tiles(center, radius)
        return [pair for pair in nearby_tiles if pair.tile.is_solid]

    def get_special_tiles(self, center, radius):
        nearby_tiles = self.get_nearby_tiles(center, radius)
        return [pair for pair in nearby_tiles if pair.tile.is_special]
