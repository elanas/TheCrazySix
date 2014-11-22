

class Action(object):
    DELETE_TYPE = "delete"
    SET_TYPE = "set"
    COMBO_SET = "combo_set"

    def __init__(self, type, row=-1, col=-1, old_tile=None, new_tile=None, num_sets=1):
        self.type = type
        self.row = row
        self.col = col
        self.old_tile = old_tile
        self.new_tile = new_tile
        self.num_sets = num_sets
