from .Piece import *

class King(Piece):
    def __init__(self, owner: Owner, board: Board,  x: int = 0, y: int = 0):
        super().__init__(owner, board, x, y)
        self.can_promote = False

    def get_normal_move_set(self):
        dir = get_owner_direction_mult(self.owner)
        one_fwd = self.y + 1 * dir
        one_bck = self.y - 1 * dir
        one_lft = self.x - 1 * dir
        one_rgt = self.x + 1 * dir
        return [Move(one_lft, one_fwd),
                Move(self.x, one_fwd),
                Move(one_rgt, one_fwd),
                Move(one_lft, self.y),
                Move(one_rgt, self.y),
                Move(one_lft, one_bck),
                Move(self.x, one_bck),
                Move(one_rgt, one_bck)]

    def get_promoted_move_set(self):
        return []

    def __str__(self):
        s = " k"
        return s

    @staticmethod
    def __generic_fen_repr__():
        return "k"
