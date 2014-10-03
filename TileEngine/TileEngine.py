from TileManager import TileManager
from asset_loader import AssetLoader


class TileEngine(object):

    def __init__(self, definitionPath, mapPath,
                 spritesheet_path, num_rows, num_cols):
        self.spritesheet_path = spritesheet_path
        self.num_cols = num_cols
        self.num_rows = num_rows
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

    def get_tile_rect(self):
        return self.tile_rect

    def get_tile_image(self, x_coords, y_coords):
        num_rows = len(self.tileMap)
        num_cols = len(self.tileMap[0])
        row_num = int(y_coords / self.tile_rect.height) % num_rows
        col_num = int(x_coords / self.tile_rect.width) % num_cols
        image = None
        try:
            image = self.tileMap[row_num][col_num].image
        except (IndexError, TypeError):
            raise Exception("The position (" + str(row_num) + ", " + str(col_num) + ")"
                            + " is not a valid position in the tile map.")
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
        