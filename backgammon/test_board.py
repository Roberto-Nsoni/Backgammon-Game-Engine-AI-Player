from board import Board, WHITE, BLACK, DiceCup, Move, Jump, Dice # type: ignore ###################
from show import show # type: ignore #####################

# these are just some sample tests

def test_dice_is_valid():
    """Check if dice.is_valid works."""

    assert Dice(1, 1).is_valid()
    assert Dice(6, 6).is_valid()
    assert Dice(1, 6).is_valid()
    assert Dice(6, 1).is_valid()
    assert not Dice(0, 1).is_valid()
    assert not Dice(1, 0).is_valid()
    assert not Dice(7, 1).is_valid()
    assert not Dice(1, 7).is_valid()


def test_dice_is_double():
    """Check if dice.is_double works."""

    assert Dice(1, 1).is_double()
    assert Dice(6, 6).is_double()
    assert not Dice(1, 2).is_double()
    assert not Dice(3, 4).is_double()


def test_validate_moves():
    """Check if board.valid_moves works"""
    # Cas general
    board = Board(Dice(6, 2), cells=[0, 0, -2, -4, -4, -1, 0, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 0, 2])
    assert board.is_valid_move(Move(jumps=[Jump(point=18, pips=6), Jump(point=18, pips=2)]))
    assert not board.is_valid_move(Move(jumps=[Jump(point=18, pips=2), Jump(point=20, pips=2)])) # Doble dau invàlid
    assert not board.is_valid_move(Move(jumps=[Jump(point=-1, pips=2), Jump(point=18, pips=6)])) # Treure desde la barra sense fitxes en ella
    assert not board.is_valid_move(Move(jumps=[Jump(point=18, pips=6), Jump(point=23, pips=2)])) # Fer un "bear off" invàlid

    # Sense moviments possibles
    board = Board(Dice(3,3), cells=[-1, 3, -1, -1, -4, 0, 3, 0, 0, -5, 0, 5, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 4], barB = 1)
    assert len(board.valid_moves()) == 1 and board.is_valid_move(Move(jumps=[]))
    board = Board(Dice(6,3), 1, [-2, 0, -2, -2, 0, -5, -2, 0, 0, 0, 0, 0, 0, 0, -1, -1, 4, 0, 9, 0, 0, 0, 1, 0], 1, 0)
    assert len(board.valid_moves()) == 1 and board.is_valid_move(Move(jumps=[]))

    # Casos MOLT específics amb pocs moviments disponibles
    # Bear off normal
    board = Board(Dice(5, 4), 58, [-5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 0, 0)
    assert len(board.valid_moves()) == 2
    assert board.is_valid_move(Move(jumps=[Jump(point=23, pips=5), Jump(point=23, pips=4)]))
    assert board.is_valid_move(Move(jumps=[Jump(point=23, pips=4), Jump(point=23, pips=5)]))

    # Bear off travieso
    board = Board(Dice(4,5), 27, [0, 0, -3, 0, 0, -10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, -2], 0, 0)
    assert len(board.valid_moves()) == 4
    assert board.is_valid_move(Move(jumps=[Jump(point=18, pips=4), Jump(point=20, pips=5)]))
    assert board.is_valid_move(Move(jumps=[Jump(point=20, pips=4), Jump(point=20, pips=5)]))
    assert board.is_valid_move(Move(jumps=[Jump(point=20, pips=5), Jump(point=18, pips=4)]))
    assert board.is_valid_move(Move(jumps=[Jump(point=20, pips=5), Jump(point=20, pips=4)]))
   
    # Un únic moviment possible amb 3 salts
    board = Board(Dice(4,4), cells=[0, -2, 0, -3, 2, -3, 0, 0, -5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 3, -2, 3, 0, 2, 0])
    assert len(board.valid_moves()) == 1
    assert board.is_valid_move(Move(jumps=[Jump(point=18, pips=4), Jump(point=18, pips=4), Jump(point=18, pips=4)]))
    
    # Un únic moviment possible amb 1 salt, cal jugar el del dau més gran
    board = Board(Dice(4, 6), cells=[0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0])
    assert board.is_valid_move(Move(jumps=[Jump(point=5, pips=6)]))
    assert not board.is_valid_move(Move(jumps=[Jump(point=5, pips=4)]))

def test_play():
    """Check if board.play works to check if the board uptades correctly afer
    every move."""

    # Captura
    board = Board(Dice(1, 3), cells=[-2, 0, 0, -2, 0, -2, 0, -2, 0, 0, 0, 3, -1, 1, 0, 1, 0, 6, 3, 0, 0, -2, 1, 0])
    move = Move([Jump(11, 1), Jump(12, 3)])
    board = board.play(move)
    assert board.bar(BLACK) == 1

    # "Treure de barra" amb captura
    board = Board(Dice(5, 2), cells=[0, -4, 0, 0, -1, -5, -1, 0, -1, 2, 0, 0, -3, 0, 0, 0, 0, 0, 5, 1, 4, 0, 1, 1], barW = 1)
    assert board.bar(BLACK) == 0 and board.bar(WHITE) == 1
    move = (Move([Jump(-1, 5), Jump(20, 2)]))
    board = board.play(move)
    assert board.bar(BLACK) == 1 and board.bar(WHITE) == 0

    # "Bear off"
    board = Board(Dice(6, 3), cells=[0, -2, 0, 0, 0, -2, -3, 0, -1, 0, -4, 0, 0, 0, 0, 0, 1, 0, 9, -3, 0, 2, 3, 0])
    assert board.off(WHITE) == board.off(BLACK) == 0
    move = (Move([Jump(16, 6), Jump(21, 3)]))
    board = board.play(move)
    assert board.off(WHITE) == 1 and board.off(BLACK) == 0

    # Final de partida amb (-1, 0, .... 0, 1)
    board = Board(Dice(6, 1), cells=[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    move = (Move([Jump(23, 6)]))
    board = board.play(move)
    assert board.over()
    assert board.winner() == WHITE

def test_over():
    """Check if board.over and board.winner works"""
    # Comprobar si la partida ha acabat
    board = Board(Dice(2, 5),turn = 22, cells=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 2, 1, 0], barB=5)
    assert not board.over()
    board = Board(Dice(2, 3))
    assert not board.over()

    # Torn dels negres que han perdut
    board = Board(Dice(2, 5),turn = 22, cells=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4])
    assert board.over() and board.winner() == WHITE
    board = board.flip()
    assert board.over() and board.winner() == BLACK
    
    # Torn dels blanques que han guanyat
    board = Board(Dice(2, 5),turn = 21, cells=[-5, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], barB=7)
    assert board.over() and board.winner() == WHITE
    board = board.flip()
    assert board.over() and board.winner() == BLACK

if __name__ == "__main__":
   ...