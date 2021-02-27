from Board import *
from Owner import *
from Pawn import *

board = Board()

for i in range(9):
    board.move_piece(Pawn(Owner.SENTE), Move(i, 2, (i %2 == 0)))
    board.move_piece(Pawn(Owner.GOTE), Move(i, 6))
board.move_piece(Pawn(Owner.GOTE), Move(0, 5, True))
board.move_piece(Pawn(Owner.SENTE), Move(2, 5))
board.move_piece(Pawn(Owner.GOTE), Move(0, 1), False)
print("""
=========[ SENTE ]========
{}
=========[ GOTE ]=========
""".format(board))

test = board.try_move(board.get_piece(1,6), Move(1,5)) #good
print("{}".format(test))
test = board.try_move(board.get_piece(2,6), Move(2,5)) #good
print("{}".format(test))
test = board.try_move(board.get_piece(0,6), Move(0,7)) #bad
print("{}".format(test))
test = board.try_move(board.get_piece(0,6), Move(0,7)) #bad
print("{}".format(test))
test = board.try_move(board.get_piece(0,1), Move(0,0)) #good, promoted
print("{}".format(test))
test = board.try_move(board.get_piece(0,5), Move(1,4)) #good
print("{}".format(test))

print("""
=========[ SENTE ]========
{}
=========[ GOTE ]=========
""".format(board))