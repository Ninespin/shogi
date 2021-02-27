
class Move:
    def __init__(self, x: int, y: int, promote: bool = False, demote: bool = False):
        self.x = x
        self.y = y
        self.promote = promote
        self.demote = demote