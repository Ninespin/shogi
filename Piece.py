from Owner import *
from Move import *


class Piece:
    def __init__(self, owner: Owner, x: int, y: int):
        self.owner = owner
        self.x = x
        self.y = y
        self.can_promote = False
        self.promoted = False

    def get_promoted_move_set(self):
        moves: list[Move] = []
        return moves

    def get_normal_move_set(self):
        moves: list[Move] = []
        return moves

    def get_current_move_set(self):
        if self.promoted:
            return self.get_promoted_move_set()
        return self.get_normal_move_set()

    def can_move(self, newx: int, newy: int):
        valid = False
        for move in self.get_current_move_set():
            if move.x is newx and move.y is newy:
                valid = True
                break
        return valid;

    def promote(self):
        self.promoted = self.can_promote

    def demote(self):
        self.promoted = False

    def move(self, move: Move):
        self.x = move.x
        self.y = move.y
        if move.promote:
            self.promote()
        elif move.demote:
            self.demote()

    def __str__(self):
        return "??"