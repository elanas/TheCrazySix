from asset_loader import AssetLoader


class TileType(object):
    EMPTY_ATTR = "empty"
    STAIR_UP_ATTR = "stair"
    STAIR_DOWN_ATTR = "stair_down"
    COIN_ATTR = "coin"
    BASE_ATTR = "base"
    START_ATTR = "player_start"
    SPAWN_ATTR = "enemy_spawn"
    LEVER_LEFT_ATTR = "switch"
    LEVER_RIGHT_ATTR = "switch_on"
    SLIDING_DOOR_ATTR = "sliding_door"
    HEALTH_ATTR = "health_replace"
    TRAP_ATTR = "trap"
    ACTION_ATTR = "action"
    LOCKED_ATTR = "locked"
    KEY_ATTR = "key_replace"
    TURRET_LEFT = "turret_spawn_left"
    TURRET_RIGHT = "turret_spawn_right"
    REPLACE_POSTFIX = "_replace"
    BASE_POSTFIX = "_base"
    EMPTY_TILE = "a"

    def __init__(self, loader, symbol, img_path, is_solid, special_attr):
        self.symbol = symbol
        self.is_solid = is_solid
        self.image = None
        self.special_attr = special_attr
        self.replace_attr = None
        self.check_special_attr()
        if loader is not None and img_path is not None:
            self.load_image(loader, img_path)

    def check_special_attr(self):
        found_replace = False
        for attr in self.special_attr:
            if attr.endswith(TileType.REPLACE_POSTFIX):
                if found_replace:
                    raise Exception("There cannot be two replace attributes")
                found_replace = True
                self.replace_attr = attr[0:-len(TileType.REPLACE_POSTFIX)] + \
                    TileType.BASE_POSTFIX

    def load_image(self, loader, img_path):
        self.image = loader.load_image(img_path)

    def get_replace_type(self):
        pass

    @property
    def is_empty(self):
        return self is TileType.EMPTY_TILE

    @property
    def is_special(self):
        return self.special_attr is not None and \
            not self.is_empty

    @property
    def is_replaceable(self):
        return self.replace_attr is not None

    @property
    def is_stair(self):
        return self.special_attr is not None and \
            TileType.STAIR_ATTR in self.special_attr

TileType.EMPTY_TILE = TileType(None, None, None, True,
                               set(TileType.EMPTY_ATTR))
