from .Piece import *


class Bishop(Piece):
    def __init__(self, owner: Owner, board: Board, x: int = 0, y: int = 0):
        super().__init__(owner, board, x, y)
        self.can_promote = True

    def get_normal_move_set(self):
        dir = get_owner_direction_mult(self.owner)
        moves = []
        moves += self.board.get_moves_in_direction(self, dir, dir)    # forward right
        moves += self.board.get_moves_in_direction(self, dir, -dir)   # forward left
        moves += self.board.get_moves_in_direction(self, -dir, dir)   # backward right
        moves += self.board.get_moves_in_direction(self, -dir, -dir)   # backward left
        return moves

    def get_promoted_move_set(self):
        dir = get_owner_direction_mult(self.owner)
        one_fwd = self.y + 1 * dir
        one_bck = self.y - 1 * dir
        one_lft = self.x - 1 * dir
        one_rgt = self.x + 1 * dir
        moves = [Move(one_lft, 0),
                 Move(one_rgt, 0),
                 Move(0, one_fwd),
                 Move(0, one_bck)]
        moves += self.get_normal_move_set()
        return moves

    def __str__(self):
        s = ("+b" if self.promoted else " b")
        return s