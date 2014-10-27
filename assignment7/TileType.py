from asset_loader import AssetLoader


class TileType(object):
    EMPTY_ATTR = "empty"
    STAIR_ATTR = "stair"
    COIN_ATTR = "coin"
    BASE_ATTR = "base"
    START_ATTR = "player_start"
    SPAWN_ATTR = "enemy_spawn"
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

    @property
    def is_empty(self):
        return self is TileType.EMPTY_TILE

    @property
    def is_special(self):
        return self.special_attr is not None and \
            not self.is_empty

    @property
    def is_stair(self):
        return self.special_attr is not None and \
            TileType.STAIR_ATTR in self.special_attr

TileType.EMPTY_TILE = TileType(None, None, None, True, 
                               list(TileType.EMPTY_ATTR))
