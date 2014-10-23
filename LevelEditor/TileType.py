

class TileType(object):
    EMPTY_ATTR = "empty"
    STAIR_ATTR = "stair"

    EMPTY_TILE = "a"

    def __init__(self, loader, symbol, img_path, is_solid, special_attr):
        self.symbol = symbol
        self.is_solid = is_solid
        self.image = None
        self.image_path = img_path
        self.special_attr = special_attr
        if loader is not None and img_path is not None:
            self.load_image(loader, img_path)

    def load_image(self, loader, img_path):
        self.image = loader.load_image(img_path)

    def __str__(self):
        if self is TileType.EMPTY_TILE:
            return "empty tile"
        attr = "none"
        if self.special_attr is not None:
            attr = self.special_attr
        return "solid: %s --- attr: %s --- img: %s" % (str(self.is_solid), attr, self.image_path)

    @property
    def is_empty(self):
        return self is TileType.EMPTY_TILE

    @property
    def is_special(self):
        return self.special_attr is not None and \
            self.special_attr != TileType.EMPTY_ATTR

    @property
    def is_stair(self):
        return self.special_attr is not None and \
            self.special_attr is TileType.STAIR_ATTR

    @staticmethod
    def create_empty(loader):
        if TileType.EMPTY_TILE.image is None:
            TileType.EMPTY_TILE.image = loader.load_image("transparent.png")

TileType.EMPTY_TILE = TileType(None, None, None, True, TileType.EMPTY_ATTR)
