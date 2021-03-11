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

fen = "lnsgk2nl/1r4gs1/p1pppp1pp/1p4p2/7P1/2P6/PP1PPPP1P/1SG4R1/LN2KGSNL b Bb"
print("loading SFEN: {}".format(fen))
board.from_fen(fen)
print_board(board)

fen = "ln1g5/1r2S1k2/p2pppn2/2ps2p2/1p7/2P6/PPSPPPPLP/2G2K1pr/+LN4+G1b w BGSLPnp"
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
        match = re.match("^(?P<piece>\+{0,1}[PpNnLlSsBbRrKkGg])(?P<originx>[1-9])(?P<originy>[1-9])(?P<move>[x\-*'])(?P<destinationx>[1-9])(?P<destinationy>[1-9])(?P<promotion>[\+\=]{0,1}$)", value)
        if match:
            piece_fen = match.group('piece')
            ox = int(match.group('originx'))-1
            oy = int(match.group('originy'))-1
            dx = int(match.group('destinationx'))-1
            dy = int(match.group('destinationy'))-1
            is_drop = match.group('move') in ['*', '\'']
            is_move = match.group('move') in ['-', 'x']
            is_take = match.group('move') == 'x'
            want_promote = match.group('promotion') == '+'
            action_success = False

            if is_move:
                piece_at_origin = board.get_piece(ox, oy)
                piece_at_dest = board.get_piece(dx, dy)
                if piece_at_origin is not None and board.get_fen_of_piece(piece_at_origin) == piece_fen:
                    if (piece_at_dest is not None) == is_take:
                        if (piece_at_dest is not None and piece_at_dest.owner != piece_at_origin.owner) or piece_at_dest is None:
                            action_success = board.try_move(piece_at_origin, Move(dx, dy, want_promote), want_promote)
                            if not action_success:
                                print("Cannot {} to {}{} with piece '{}' at {}{} : invalid movement.".format(("take" if is_take else "move"), dx+1, dy+1, piece_fen, ox+1, oy+1))
                    else:
                        print("Cannot {} square {}{}".format("take empty" if is_take else "move to occupied", dx+1, dy+1))
                else:
                    print("No such piece '{}' at origin {}{}.{}{}{}".format(piece_fen, ox+1, oy+1,board.get_fen_of_piece(piece_at_origin) == piece_fen ,board.get_fen_of_piece(piece_at_origin), piece_fen))
            elif is_drop:
                sideboard_piece = board.get_from_sideboard(piece_fen)
                if sideboard_piece is not None:
                    action_success = board.drop(sideboard_piece, dx+1, dy+1)
                    if not action_success:
                        print("Cannot drop piece '{}' from {}'s sideboard to {}{}.".format(piece_fen, Owner.SENTE.name if piece_fen.isupper() else Owner.GOTE.name, dx+1, dy+1))
                else:
                    print("No piece '{}' in {}'s sideboard.".format(piece_fen, Owner.SENTE.name if piece_fen.isupper() else Owner.GOTE.name))
            if action_success:
                board.current_player = Owner.GOTE if board.current_player == Owner.SENTE else Owner.SENTE
                print("Action successful!")
        print_board(board)

