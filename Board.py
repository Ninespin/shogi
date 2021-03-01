from Config import *
from Pieces import Piece
from Owner import *
from Move import *


class Board:
    def __init__(self):
        self.sizex = BOARD_SIZE_X_MAX
        self.sizey = BOARD_SIZE_Y_MAX
        self.promotezone = BOARD_PROMOTE_ZONE_DEPTH
        self.sentepromotion = self.sizey-self.promotezone
        self.gotepromotion = self.promotezone
        self.data: list[list[Piece]] = [[None for i in range(self.sizex)] for j in range(self.sizey)]
        self.gotesideboard: list[Piece] = []
        self.sentesideboard: list[Piece] = []

    def get_piece(self, x: int, y: int) -> Piece:
        return self.data[y][x]

    def set_piece(self, x: int, y: int, piece: Piece):
        self.data[y][x] = piece

    def try_promote_piece_at(self, x: int, y: int):
        if self.data[y][x] is not None:
            self.data[y][x].promote()
            return True
        return False

    def is_promote(self, piece: Piece, move: Move) -> bool:
        if piece.owner is Owner.GOTE:
            return move.y >= self.gotepromotion or piece.y >= self.promotezone
        elif piece.owner is Owner.SENTE:
            return move.y < self.sentepromotion or piece.y < self.promotezone

    def is_move_valid(self, piece: Piece, move: Move):
        return self.is_move_in_board_and_not_on_ally(piece, move) and piece.can_move(move.x, move.y)

    def is_move_in_board_and_not_on_ally(self, piece: Piece, move: Move) -> bool:
        if (0 <= move.x < self.sizex) and (0 <= move.y < self.sizey):
            piece_at_pos = self.get_piece(move.x, move.y)
            return piece_at_pos is None or piece_at_pos.owner is not piece.owner
        return False

    def filter_valid_moves(self, piece: Piece, suggest_promote: bool = False):
        moveset = piece.get_current_move_set()
        valid: list[Move] = []
        for move in moveset:
            if self.is_move_in_board_and_not_on_ally(piece, move):
                valid.append(move)
                if suggest_promote and not move.promote and self.is_promote(piece, move):
                    valid.append(Move(move.x, move.y, True))
        return valid

    def get_moves_in_direction(self, piece: Piece, dx: int, dy: int):
        moves = []
        curr_x = piece.x + dx
        curr_y = piece.y + dy
        if dx == 0 and dy == 0:
            return moves

        while 0 <= curr_x < BOARD_SIZE_X_MAX and 0 <= curr_y < BOARD_SIZE_Y_MAX:
            possible_piece = self.get_piece(curr_x, curr_y)
            if possible_piece is not None:
                if possible_piece.owner is not piece.owner:
                    moves.append(Move(curr_x, curr_y))
                break
            else:
                moves.append(Move(curr_x, curr_y))
            curr_x += dx
            curr_y += dy
        return moves

    def capture(self, capturer: Piece, captured: Piece):
        if capturer.owner is Owner.GOTE:
            self.gotesideboard.append(captured)
        elif capturer.owner is Owner.SENTE:
            self.sentesideboard.append(captured)

    def place_piece(self, piece: Piece, move: Move, promote: bool = False):
        piece_at_pos = self.get_piece(move.x, move.y)
        if piece_at_pos is not None:
            self.capture(piece, piece_at_pos)
        self.set_piece(move.x, move.y, piece)
        piece.move(move)
        if promote:
            piece.promote()

    def move_piece(self, piece: Piece, move: Move, enable_promotion: bool = True):
        piece_at_pos = self.get_piece(move.x, move.y)
        if piece_at_pos is not None and piece_at_pos.owner is not piece.owner:
            self.capture(piece, piece_at_pos)
        self.set_piece(move.x, move.y, piece)
        self.set_piece(piece.x, piece.y, None)
        piece.move(move)
        if enable_promotion and not self.filter_valid_moves(piece): #dont suggest promotion
            piece.promote()

    def try_move(self, piece: Piece, move: Move, enable_promotion: bool = True) -> bool:
        can_move = self.is_move_valid(piece, move)
        if can_move:
            self.move_piece(piece, move, enable_promotion)
        return can_move

    def __str__(self):
        s = ""
        for i in reversed(range(self.sizex)):
            s += " {} ".format(i+1)
        s += "\n"
        for j in range(self.sizey):
            for i in reversed(range(self.sizex)):
                piece = self.get_piece(i, j)
                piece_str = ((str(piece).upper() if piece.owner is Owner.GOTE else str(piece))+" ") if piece is not None else " . "
                s += piece_str
            s += " {}\n".format(j+1)
        return s