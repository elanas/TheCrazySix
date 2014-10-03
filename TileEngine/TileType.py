from asset_loader import AssetLoader


class TileType(object):

    def __init__(self, symbol, tile_id, solid, tile_sprite_sheet):
        self.symbol = symbol
        self.tile_id = tile_id
        self.solid = solid
        self.image = None
        self.set_image(tile_sprite_sheet)

    def set_image(self, tile_sprite_sheet):
        try:
            self.image = tile_sprite_sheet[self.tile_id]
        except (IndexError, TypeError):
            raise IndexError("The tile spritesheet does not contain an " +
                             "image in position " + str(self.tile_id) + ".")
