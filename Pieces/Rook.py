from .Piece import *


class Rook(Piece):
    def __init__(self, owner: Owner, board: Board, x: int = 0, y: int = 0):
        super().__init__(owner, board, x, y)
        self.can_promote = True

    def get_normal_move_set(self):
        dir = get_owner_direction_mult(self.owner)
        moves = []
        moves += self.board.get_moves_in_direction(self, 0, dir)    # forward
        moves += self.board.get_moves_in_direction(self, 0, -dir)   # back
        moves += self.board.get_moves_in_direction(self, -dir, 0)   # left
        moves += self.board.get_moves_in_direction(self, dir, 0)   # right
        return moves

    def get_promoted_move_set(self):
        dir = get_owner_direction_mult(self.owner)
        one_fwd = self.y + 1 * dir
        one_bck = self.y - 1 * dir
        one_lft = self.x - 1 * dir
        one_rgt = self.x + 1 * dir
        moves = [Move(one_lft, one_fwd),
                 Move(one_rgt, one_fwd),
                 Move(one_lft, one_bck),
                 Move(one_rgt, one_bck)]
        moves += self.get_normal_move_set()
        return moves

    def __str__(self):
        s = ("+r" if self.promoted else " r")
        return s

    @staticmethod
    def __generic_fen_repr__():
        return "r"
