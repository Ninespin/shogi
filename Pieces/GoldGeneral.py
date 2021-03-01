from .Piece import *


class GoldGeneral(Piece):
    def __init__(self, owner: Owner, board: Board, x: int = 0, y: int = 0):
        super().__init__(owner, board, x, y)
        self.can_promote = False

    def get_normal_move_set(self):
        dir = get_owner_direction_mult(self.owner)
        one_fwd = self.y + 1 * dir
        one_bck = self.y - 1 * dir
        return [Move(self.x - 1, one_fwd),
                Move(self.x, one_fwd),
                Move(self.x + 1, one_fwd),
                Move(self.x - 1, self.y),
                Move(self.x + 1, self.y),
                Move(self.x, one_bck)]

    def get_promoted_move_set(self):
        return []

    def __str__(self):
        s = " g"
        return s
