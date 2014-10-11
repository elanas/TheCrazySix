from TileType import TileType
from os import path
from asset_loader import AssetLoader


class TileManager(object):
    TILE_ID_INDEX = 0
    SOLID_INDEX = 1
    COMMENT_CHAR = '#'

    def __init__(self, definitionPath, mapPath):
        self.loader = AssetLoader(path.join("images", "tiles"))
        self.tileDefinitions = list()
        self.definitionPath = definitionPath
        self.mapPath = mapPath
        self.tileDefinitions = dict()
        self.tileMap = list()
        self.readTileDefinitions()
        self.readTileMap()

    def readTileDefinitions(self):
        lines = [line.strip() for line in open(self.definitionPath)]
        for definition in lines:
            if len(definition) == 0 or \
                    definition[0] == TileManager.COMMENT_CHAR:
                continue
            fields = definition.split()
            if not len(fields) == 3 and not len(fields) == 4:
                raise Exception(
                    "The tile engine definition file is incorrectly formed")
            if len(fields) == 3:
                fields.append(None)
            symbol, img_path, solidStr, specialField = fields
            if symbol is "/" or symbol is "'\'":
                specialField = "stair"
            solid = not int(solidStr) == 0
            curr_tile = \
                TileType(self.loader, symbol, img_path, solid, specialField)
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
                    self.tileMap[rowNum].append(None)
                else:
                    self.tileMap[rowNum].append(self.getTile(row[i]))
            rowNum += 1

    def getTileMap(self):
        return self.tileMap

    def getTileRect(self):
        return self.tileDefinitions.itervalues().next().image.get_rect()

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
