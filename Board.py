from Config import *
from Pieces import *
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
        self.gote_sideboard: list[Piece] = []
        self.sente_sideboard: list[Piece] = []
        self.current_player: Owner = Owner.SENTE

    def from_fen(self, fen: str):
        self.clear()
        piece_factory: PieceFactory = PieceFactory()
        parts = fen.split()
        # board state
        lines = parts[0].split('/')
        for row, line in enumerate(lines):
            current_piece = ""
            piece_complete = False
            previous_is_skip = False
            column = 0
            if line.isnumeric():
                column += int(line)
            else:
                for i in range(len(line)):
                    if line[i] == "+":
                        if previous_is_skip:
                            column += int(current_piece)
                            previous_is_skip = False
                            current_piece = ""
                        current_piece += line[i]
                    elif piece_factory.is_known_fen(line[i]):
                        if previous_is_skip:
                            column += int(current_piece)
                            previous_is_skip = False
                            current_piece = ""
                        current_piece += line[i]
                        piece_complete = True
                    elif line[i].isnumeric():
                        current_piece += line[i]
                        previous_is_skip = True

                    if piece_complete:
                        piece: Piece = piece_factory.make_piece_from_fen(current_piece, self)
                        self.set_piece(self.sizex - column - 1, row, piece)
                        current_piece = ""
                        piece_complete = False
                        column += 1

        # current player
        if len(parts) > 1:
            if parts[1] == "w":
                self.current_player = Owner.GOTE
            elif parts[1] == "b":
                self.current_player = Owner.SENTE
        # sideboards
        if len(parts) > 2:
            hands = parts[2]
            for i, p in enumerate(hands):
                piece: Piece = piece_factory.make_piece_from_fen(p, self, -1, -1)
                if piece is not None:
                    if piece.owner is Owner.GOTE:
                        self.gote_sideboard.append(piece)
                    elif piece.owner is Owner.SENTE:
                        self.sente_sideboard.append(piece)

    def clear(self):
        self.data: list[list[Piece]] = [[None for i in range(self.sizex)] for j in range(self.sizey)]
        self.gote_sideboard: list[Piece] = []
        self.sente_sideboard: list[Piece] = []

    def get_piece(self, x: int, y: int) -> Piece:
        return self.data[y][x]

    def set_piece(self, x: int, y: int, piece: Piece):
        if piece is not None:
            piece.x = x
            piece.y = y
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
        if (0 <= move.x < self.sizex) and (0 <= move.y < self.sizey) and piece is not None:
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
            self.gote_sideboard.append(captured)
        elif capturer.owner is Owner.SENTE:
            self.sente_sideboard.append(captured)

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
        if move not in self.filter_valid_moves(piece, enable_promotion):
            move.promote = False
        if piece_at_pos is not None and piece_at_pos.owner is not piece.owner:
            self.capture(piece, piece_at_pos)
        self.set_piece(piece.x, piece.y, None)
        self.set_piece(move.x, move.y, piece)
        piece.move(move)
        if enable_promotion and not self.filter_valid_moves(piece): #cant move and enable promote
            piece.promote()

    def try_move(self, piece: Piece, move: Move, enable_promotion: bool = True) -> bool:
        can_move = self.is_move_valid(piece, move)
        if can_move:
            self.move_piece(piece, move, enable_promotion)
        return can_move

    def drop(self, piece: Piece, x: int, y: int):
        if piece.owner == Owner.SENTE:
            sideboard = self.sente_sideboard
        else:
            sideboard = self.gote_sideboard
        good_to_drop = False
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            piece_at_dest = self.get_piece(x, y)
            if piece_at_dest is None and piece in sideboard:
                if isinstance(piece, Pawn): # pawn drop special rule
                    for j in range(self.sizey):
                        ptarg = self.get_piece(x, j)
                        good_to_drop = not (isinstance(ptarg, Pawn) and piece.owner == ptarg.owner and not ptarg.promoted)
                        if not good_to_drop:
                            break
                else:
                    good_to_drop = True
                if good_to_drop:
                    sideboard.remove(piece)
                    self.place_piece(piece, Move(x, y))
        return good_to_drop

    def get_fen_of_piece(self, piece: Piece):
        return ((str(piece).upper() if piece.owner is Owner.SENTE else str(
            piece))) if piece is not None else "."

    def get_fen_of_piece_at_pos(self, x: int, y: int):
        return self.get_fen_of_piece(self.get_piece(x, y))

    def is_in_sideboard(self, piece: Piece):
        if piece.owner == Owner.GOTE:
            sideboard = self.gote_sideboard
        else:
            sideboard = self.sente_sideboard
        return piece in sideboard

    def get_from_sideboard(self, sfen: str):
        if sfen.isupper():
            sideboard = self.sente_sideboard
        else:
            sideboard = self.gote_sideboard
        for piece in sideboard:
            if self.get_fen_of_piece(piece) == sfen:
                return piece
        return None

    def get_sideboard_str(self, owner: Owner):
        sideboard = self.sente_sideboard if owner is Owner.SENTE else self.gote_sideboard
        s = "[" + (" " if len(sideboard) == 0 else "")
        for piece in sideboard:
            s += (str(piece).upper() if piece.owner is Owner.SENTE else str(piece)) + " "
        s += "]"
        return s

    def __str__(self):
        s = ""
        for i in reversed(range(self.sizex)):
            s += " {} ".format(i+1)
        s += "\n"
        for j in range(self.sizey):
            for i in reversed(range(self.sizex)):
                piece = self.get_piece(i, j)
                piece_str = ((str(piece).upper() if piece.owner is Owner.SENTE else str(
                        piece))) if piece is not None else "."
                s += (" " if (piece is None or not piece.promoted) else "") + piece_str + " "
            s += " {}{}".format(j+1, '\n' if j < self.sizey - 1 else '')
        return s
