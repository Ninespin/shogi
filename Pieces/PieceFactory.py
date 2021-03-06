from .Piece import *
from .Bishop import *
from .GoldGeneral import *
from .Lance import *
from .King import *
from .Knight import *
from .Pawn import *
from .Rook import *
from .SilverGeneral import *
from Owner import *
import Board


class PieceFactory:
    def __init__(self):
        self.map = {Bishop.__generic_fen_repr__(): Bishop,
                    GoldGeneral.__generic_fen_repr__(): GoldGeneral,
                    King.__generic_fen_repr__(): King,
                    Knight.__generic_fen_repr__(): Knight,
                    Lance.__generic_fen_repr__(): Lance,
                    Pawn.__generic_fen_repr__(): Pawn,
                    Rook.__generic_fen_repr__(): Rook,
                    SilverGeneral.__generic_fen_repr__(): SilverGeneral}

    def ctor_from_fen(self, fen: str):
        return self.map[fen]

    def is_known_fen(self, fen: str):
        return fen.lower() in self.map.keys()

    def make_piece_from_fen(self, fen: str, board: Board, x: int = 0, y: int = 0):
        promoted = fen.startswith('+')
        fen = fen[1:] if promoted else fen
        piece: Piece = None
        if self.is_known_fen(fen):
            owner: Owner = Owner.SENTE if fen.isupper() else Owner.GOTE
            piece = self.ctor_from_fen(fen.lower())(owner, board, x, y)
            if promoted:
                piece.promote()
        return piece
