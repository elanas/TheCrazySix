from asset_loader import AssetLoader


class TileType(object):
    EMPTY_ATTR = "empty"
    STAIR_ATTR = "stair"

    EMPTY_TILE = "a"    

    def __init__(self, loader, symbol, img_path, is_solid, special_attr):
        self.symbol = symbol
        self.is_solid = is_solid
        self.image = None
        self.special_attr = special_attr
        if loader is not None and img_path is not None:
            self.load_image(loader, img_path)

    def load_image(self, loader, img_path):
        self.image = loader.load_image(img_path)

    def is_empty(self):
        return self is TileType.EMPTY_TILE

TileType.EMPTY_TILE = TileType(None, None, None, True, TileType.EMPTY_ATTR)