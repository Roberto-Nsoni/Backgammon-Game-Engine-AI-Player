from board import Board, WHITE, BLACK, DiceCup, Move, Jump, Dice # type: ignore ###################
from show import show

# these are just some sample tests

def test_validate_moves(board: Board):
    """Check if board.valid_moves works"""
    for move in board.valid_moves():
        print(move)
    print()

def test_over():
    """Check if board.over and board.winner works"""
    # Comprobar si la partida ha acabat
    board = Board(Dice(2, 5),turn = 22, cells=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], barB=5)
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

def show_move(board: Board, move: Move) -> None:
    if move not in board.valid_moves():
        print("Jugada no vàlida")
        return
    simulated_board = board.copy().play(move).flip()

    show(simulated_board)

if __name__ == "__main__":
    '''
    test_validate_moves(Board(Dice(2, 1)))
    test_validate_moves(Board(Dice(5, 6)))
    test_validate_moves(Board(Dice(6, 3)))
    test_validate_moves(Board(Dice(4, 4)))
    '''
 
    # Bear off normal
    test_validate_moves(Board(Dice(5, 4), 58, [-5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 0, 0))
    
    # Bear off travieso
    test_validate_moves(Board(Dice(4,5), 27, [0, 0, -3, 0, 0, -10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, -2], 0, 0)) 

    # Bear off un movimiento exacto
    test_validate_moves(Board(Dice(6, 2), cells=[0, 0, -2, -4, -4, -3, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 0, 2]))

    test_validate_moves(Board(Dice(6, 2), cells=[0, 0, -2, -4, -4, -3, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 0, 2]))