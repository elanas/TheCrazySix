import pygame
from TileManager import TileManager
from asset_loader import AssetLoader


class TileEngine(object):
    EMPTY_COLOR = (0, 0, 0)

    def __init__(self, definitionPath, mapPath,
                 spritesheet_path, num_rows, num_cols, scale=1):
        self.spritesheet_path = spritesheet_path
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.scale = scale
        self.tile_spritesheet = None
        self.load_sprite_sheet()
        self.tileManager = TileManager(
            definitionPath, mapPath, self.tile_spritesheet)
        self.tileMap = self.tileManager.getTileMap()

    def load_sprite_sheet(self):
        self.loader = AssetLoader("images")
        self.tile_spritesheet = self.loader.load_spritesheet(
            self.spritesheet_path, self.num_rows, self.num_cols, False)
        self.tile_rect = self.tile_spritesheet[0].get_rect()
        self.scaleImages()

    def scaleImages(self):
        if self.scale == 1:
            return
        self.tile_rect.width *= self.scale
        self.tile_rect.height *= self.scale
        for i in range(0, len(self.tile_spritesheet)):
            self.tile_spritesheet[i] = pygame.transform.scale(
                self.tile_spritesheet[i],
                (self.tile_rect.width, self.tile_rect.height))

    def get_tile_rect(self):
        return self.tile_rect

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
        row_num = int(y_coords / self.tile_rect.height)
        col_num = int(x_coords / self.tile_rect.width)
        image = None
        tile = None
        if row_num < 0 or row_num >= num_rows or col_num < 0 or col_num >= len(self.tileMap[row_num]):
            tile = None
        else:
            tile = self.tileMap[row_num][col_num]
        if tile is None:
            image = pygame.Surface((self.tile_rect.width, self.tile_rect.height)).convert()
            image.fill(TileEngine.EMPTY_COLOR)
        else:
            image = tile.image
        area = image.get_rect().copy()
        remainder_y = y_coords % self.tile_rect.height
        remainder_x = x_coords % self.tile_rect.width
        if not remainder_y == 0:
            area.y += remainder_y
            area.height -= remainder_y
        if not remainder_x == 0:
            area.x += remainder_x
            area.width -= remainder_x
        if not remainder_x == 0 or not remainder_y == 0:
            image = image.subsurface(area)
        return image
