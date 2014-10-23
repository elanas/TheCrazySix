import pygame
from TileManager import TileManager
from TileType import TileType
from asset_loader import AssetLoader


class TileEngine(object):

    def __init__(self, definitionPath, mapPath, num_rows, num_cols):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.tileManager = TileManager(definitionPath, mapPath)
        self.tileRect = self.tileManager.getTileRect()
        self.tileMap = self.tileManager.getTileMap()

    def get_tile_rect(self):
        return self.tileRect

    def getNumRows(self):
        return len(self.tileMap)

    def getNumCols(self, row_num):
        try:
            return len(self.tileMap[row_num])
        except IndexError:
            return -1

    def getMaxCols(self):
        return max([len(row) for row in self.tileMap])

    def getBottomCenterX(self):
        last_row = self.tileMap[-1]
        print len(last_row) / 2 * self.tileRect.width
        return len(last_row) / 2 * self.tileRect.width

    def get_tile_from_attr(self, special_attr):
        definitions = self.tileManager.tileDefinitions
        for symbol in definitions:
            tile = definitions[symbol]
            if tile.special_attr == special_attr:
                return tile
        return None

    def get_tile_pos(self, x_coords, y_coords):
        tile_rect = self.get_tile_rect()
        row_num = int(y_coords / tile_rect.height)
        col_num = int(x_coords / tile_rect.width)
        return row_num, col_num

    def get_tile(self, x_coords, y_coords, set_pos=True):
        num_rows = len(self.tileMap)
        tile_rect = self.get_tile_rect().copy()
        row_num = int(y_coords / tile_rect.height)
        col_num = int(x_coords / tile_rect.width)
        tile = None
        if self.is_coord_valid(row_num, col_num):
            tile = self.tileMap[row_num][col_num]
        if tile is None:
            tile = TileType.EMPTY_TILE
        remainder_y = y_coords % tile_rect.height
        remainder_x = x_coords % tile_rect.width
        if remainder_y > 0:
            tile_rect.y += remainder_y
            tile_rect.height -= remainder_y
        if remainder_x > 0:
            tile_rect.x += remainder_x
            tile_rect.width -= remainder_x
        if set_pos:
            tile_rect.x = x_coords
            tile_rect.y = y_coords
        return tile, tile_rect

    def get_tile_image(self, x_coords, y_coords):
        tile, tile_rect = self.get_tile(x_coords, y_coords, False)
        full_tile_rect = self.get_tile_rect()
        image = tile.image
        if image is not None and \
            (tile_rect.width != full_tile_rect.width or
                tile_rect.height != full_tile_rect.height):
            image = image.subsurface(tile_rect)
        tile_rect.x = x_coords
        tile_rect.y = y_coords
        return image, tile_rect

    def is_coord_valid(self, row_num, col_num):
        return 0 <= row_num and row_num < len(self.tileMap) and \
            0 <= col_num and col_num < len(self.tileMap[row_num])
