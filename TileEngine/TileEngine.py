import pygame
from TileManager import TileManager
from asset_loader import AssetLoader


class TileEngine(object):
    EMPTY_COLOR = (0, 0, 0)

    def __init__(self, definitionPath, mapPath, num_rows, num_cols):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.tileManager = TileManager(definitionPath, mapPath)
        self.tileMap = self.tileManager.getTileMap()

    def get_tile_rect(self):
        return self.tileManager.getTileRect()

    def getNumRows(self):
        return len(self.tileMap)

    def getNumCols(self, row_num):
        try:
            return len(self.tileMap[row_num])
        except IndexError:
            return -1

    def getMaxCols(self):
        return max([len(row) for row in self.tileMap])

    def get_tile_image(self, x_coords, y_coords):
        num_rows = len(self.tileMap)
        tile_rect = self.get_tile_rect()
        row_num = int(y_coords / tile_rect.height)
        col_num = int(x_coords / tile_rect.width)
        image = None
        tile = None
        if row_num < 0 or row_num >= num_rows or col_num < 0 or col_num >= len(self.tileMap[row_num]):
            tile = None
        else:
            tile = self.tileMap[row_num][col_num]
        if tile is None:
            image = pygame.Surface((tile_rect.width, tile_rect.height)).convert()
            image.fill(TileEngine.EMPTY_COLOR)
        else:
            image = tile.image
        area = image.get_rect().copy()
        remainder_y = y_coords % tile_rect.height
        remainder_x = x_coords % tile_rect.width
        if not remainder_y == 0:
            area.y += remainder_y
            area.height -= remainder_y
        if not remainder_x == 0:
            area.x += remainder_x
            area.width -= remainder_x
        if not remainder_x == 0 or not remainder_y == 0:
            image = image.subsurface(area)
        return image
