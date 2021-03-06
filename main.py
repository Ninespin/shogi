import Board
import re
from Config import *
from Pieces import *

def print_board(b: Board):
    print("""
============[ GOTE ]========== holds {}
{}
============[ SENTE ]========= holds {}
currently playing: {}
""".format(
        b.get_sideboard_str(Owner.GOTE),
        b,
        b.get_sideboard_str(Owner.SENTE),
        b.current_player.name
    ))


board = Board.Board()

board.place_piece(Pawn(Owner.GOTE, 0, 0), Move(0, 0))
print_board(board)

board.try_move(board.get_piece(0, 0), Move(1, 1))
print_board(board)

board.try_move(board.get_piece(0, 0), Move(0, 1))
print_board(board)

board.try_move(board.get_piece(0, 1), Move(0, 0))
print_board(board)

fen = "+lnsgk2nl/1r4gs1/p1pppp1pp/1p4p2/7P1/2P6/PP1PPPP1P/1SG4R1/LN2KGSNL b Bb"
print("loading SFEN: {}".format(fen))
board.from_fen(fen)
print_board(board)

fen = "l+n1g5/1r2S1k2/p2pppn2/2ps2p2/1p7/2P6/PPSPPPPLP/2G2K1pr/+LN4+G1b w BGSLPnp"
print("loading SFEN: {}".format(fen))
board.from_fen(fen)
print_board(board)


while True:
    value = input("{}'s next move: ".format(board.current_player.name))
    if re.match("^exit", value):
        break;
    elif re.match("^help|h|\?", value):
        print("exit - exits the game")
        print("help - shows help")
        print("move format: <PIECE><ORIGIN><MOVEMENT><DESTINATION><(PROMOTION)>")
    else:
        match = re.match("^(?P<piece>\+{0,1}[PpNnLlSsBbRrKkGg])(?P<origin>[0-8]{2})(?P<move>[x\-*'])(?P<destination>[0-8]{2})(?P<promotion>\+|\=|$)", value)
        if match:
            print("""
piece: {}
origin: {}
move: {}
destination: {}
promote: {}
""".format(match.group('piece'), match.group('origin'),match.group('move'),match.group('destination'),match.group('promotion')))

