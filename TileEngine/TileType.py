from asset_loader import AssetLoader


class TileType(object):
    STAIR_ATTR = "stair"

    def __init__(self, loader, symbol, img_path, solid, special_attr):
        self.symbol = symbol
        self.solid = solid
        self.image = None
        self.special_attr = special_attr
        self.load_image(loader, img_path)

    def load_image(self, loader, img_path):
        self.image = loader.load_image(img_path)
