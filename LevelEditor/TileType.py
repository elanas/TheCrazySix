

class TileType(object):
    EMPTY_ATTR = "empty"
    STAIR_UP_ATTR = "stair"
    STAIR_DOWN_ATTR = "stair_down"
    COIN_ATTR = "coin"
    BASE_ATTR = "base"
    START_ATTR = "player_spawn"
    RESPAWN_ATTR = "player_respawn"
    SPAWN_ATTR = "enemy_spawn"
    LEVER_LEFT_ATTR = "switch"
    LEVER_RIGHT_ATTR = "switch_on"
    SLIDING_DOOR_ATTR = "sliding_door"
    HEALTH_ATTR = "health_replace"
    TRAP_ATTR = "trap"
    ACTION_ATTR = "action"
    LOCKED_ATTR = "locked"
    KEY_ATTR = "key_replace"
    TURRET_ATTR = "turret"
    TURRET_LEFT = "turret_spawn_left"
    TURRET_RIGHT = "turret_spawn_right"
    TURRET_COMBO = "turret_combo"
    TURRET_COMBO_LEFT = "turret_left_combo"
    TURRET_COMBO_RIGHT = "turret_right_combo"
    REPLACE_POSTFIX = "_replace"
    BASE_POSTFIX = "_base"
    EMPTY_SYMBOL = " "
    REDBALL_ATTR = "redball_replace"
    GREENBALL_ATTR = "redball_base"

    def __init__(self, loader, symbol, img_path, is_solid, special_attr,
                 line_num=-1):
        self.symbol = symbol
        self.is_solid = is_solid
        self.image = None
        self.image_path = img_path
        self.special_attr = special_attr
        self.line_num = line_num
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
        return "solid: %s --- attr: %s --- img: %s" % \
            (str(self.is_solid), attr, self.image_path)

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

    @staticmethod
    def create_empty(loader):
        if TileType.EMPTY_TILE.image is None:
            TileType.EMPTY_TILE.image = loader.load_image("transparent.png")

TileType.EMPTY_TILE = TileType(None, TileType.EMPTY_SYMBOL, None, True,
                               list(TileType.EMPTY_ATTR))
