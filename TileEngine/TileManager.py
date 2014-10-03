from TileType import TileType


class TileManager(object):
    TILE_ID_INDEX = 0
    SOLID_INDEX = 1

    def __init__(self, definitionPath, mapPath, tile_sprite_sheet):
        self.tileDefinitions = list()
        self.definitionPath = definitionPath
        self.mapPath = mapPath
        self.tile_sprite_sheet = tile_sprite_sheet
        self.tileDefinitions = dict()
        self.tileMap = list()
        self.defaultTile = None
        self.readTileDefinitions()
        self.readTileMap()

    def readTileDefinitions(self):
        lines = [line.strip() for line in open(self.definitionPath)]
        for definition in lines:
            if len(definition) == 0:
                continue
            fields = definition.split()
            if not len(fields) == 3:
                raise Exception(
                    "The tile engine definition file is incorrectly formed")
            symbol, tile_id_str, solidStr = fields
            tile_id = int(tile_id_str)
            solid = not int(solidStr) == 0
            curr_tile = TileType(symbol, tile_id, solid,
                                 self.tile_sprite_sheet)
            if self.defaultTile is None:
                self.defaultTile = curr_tile
            self.tileDefinitions[symbol] = curr_tile
        if len(self.tileDefinitions) == 0:
            raise Exception("The tile definition file cannot be empty.")

    def readTileMap(self):
        rowNum = 0
        lines = [line.rstrip('\r\n') for line in open(self.mapPath)]
        for row in lines:
            self.tileMap.append(list())
            for i in range(0, len(row)):
                if row[i] == ' ':
                    self.tileMap[rowNum].append(self.defaultTile)
                else:
                    self.tileMap[rowNum].append(self.getTile(row[i]))
            if not rowNum == 0 and not \
                    len(self.tileMap[rowNum]) == len(self.tileMap[rowNum - 1]):
                raise Exception(
                    "The tile map provided does not have uniform line length.")
            rowNum += 1

    def getTileMap(self):
        return self.tileMap

    def getTile(self, symbol):
        try:
            return self.tileDefinitions[symbol]
        except KeyError:
            raise Exception("No definition exists for a tile with the " +
                            "symbol \"" + symbol + "\".")

    def containsSymbol(self, symbol):
        return symbol in self.tileDefinitions

    def isSymbolSolid(self, symbol):
        try:
            return self.tileDefinitions[symbol][TileManager.SOLID_INDEX] == 1
        except KeyError:
            raise Exception(
                "No tile with the symbol \"" + symbol + "\" is defined")