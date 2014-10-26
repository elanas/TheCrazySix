

class Action(object):
    DELETE_TYPE = "delete"
    SET_TYPE = "set"

    def __init__(self, type, row, col, old_tile=None, new_tile=None):
        self.type = type
        self.row = row
        self.col = col
        self.old_tile = old_tile
        self.new_tile = new_tile
