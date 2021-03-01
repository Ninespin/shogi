import Board
from Config import *
from Pieces import *

board = Board.Board()

for i in range(BOARD_SIZE_X_MAX):
    board.place_piece(Pawn(Owner.SENTE, board), Move(i, 2, (i %2 == 0)))
    board.place_piece(Pawn(Owner.GOTE, board), Move(i, 6))
board.place_piece(Pawn(Owner.GOTE, board), Move(0, 5, True))
board.place_piece(Pawn(Owner.SENTE, board), Move(2, 5))
board.place_piece(Pawn(Owner.GOTE, board), Move(0, 1))
board.place_piece(Lance(Owner.GOTE, board), Move(8, 5))
board.place_piece(Lance(Owner.GOTE, board), Move(7, 5))
board.place_piece(Lance(Owner.GOTE, board), Move(6, 5))
board.place_piece(Lance(Owner.GOTE, board), Move(2, 8))
board.place_piece(Lance(Owner.GOTE, board), Move(3, 8))
board.place_piece(Lance(Owner.GOTE, board), Move(1, 8, True))
board.place_piece(Rook(Owner.GOTE, board), Move(4,4))
print("""
=========[ SENTE ]========
{}
=========[ GOTE ]=========
""".format(board))

#Pawns
print("Pawns")
test = board.try_move(board.get_piece(1,6), Move(1,5)) #good
print("{} must be Ture".format(test))
test = board.try_move(board.get_piece(2,6), Move(2,5)) #good
print("{} must be Ture".format(test))
test = board.try_move(board.get_piece(0,6), Move(0,7)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(0,6), Move(0,7)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(0,1), Move(0,0)) #good, promoted
print("{} must be Ture".format(test))
test = board.try_move(board.get_piece(0,5), Move(1,4)) #good
print("{} must be Ture".format(test))
#Lances
print("Lances")
test = board.try_move(board.get_piece(8,5), Move(1,4)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(8,5), Move(8,6)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(2,8), Move(2,5)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(1,8), Move(1,5)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(3,8), Move(3,5)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(7,5), Move(7,0)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(8,5), Move(8,2)) #good
print("{} must be True".format(test))
test = board.try_move(board.get_piece(6,5), Move(6,3)) #good
print("{} must be True".format(test))
#Rooks
print("Rooks")
test = board.try_move(board.get_piece(4,4), Move(4,3)) #good
print("{} must be True".format(test))
test = board.try_move(board.get_piece(4,3), Move(4,2)) #good
print("{} must be True".format(test))
test = board.try_move(board.get_piece(4,2), Move(3,1)) #good
print("{} must be False".format(test))
test = board.try_promote_piece_at(4,2)
print("{} must be True".format(test))
test = board.try_move(board.get_piece(4,2), Move(3,1)) #good
print("{} must be True".format(test))
test = board.try_move(board.get_piece(3,1), Move(3,7)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(3,1), Move(3,6)) #bad
print("{} must be False".format(test))
test = board.try_move(board.get_piece(3,1), Move(2,6)) #bad
print("{} must be False".format(test))

print("""
=========[ SENTE ]========
{}
=========[ GOTE ]=========
""".format(board))