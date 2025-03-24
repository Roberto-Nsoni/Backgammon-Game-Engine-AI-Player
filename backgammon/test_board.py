from board import Board, WHITE, DiceCup, Move, Jump, Dice # type: ignore ###################
from show import show

# these are just some sample tests

def test_validate_moves(board: Board):
    """Check if board.valid_moves works"""

    show(board)
    print("Valid moves for", board.dice())

    sorted_moves = sorted(
    board.valid_moves(),
    key=lambda move: [(jump.point, jump.pips) for jump in move.jumps]  # Ordena por todos los jumps
)
    
    for i, move in enumerate(sorted_moves):
        print(f'{i} -', end=" ")
        for jump in move.jumps:
            print(jump.point + 1, jump.pips, end=" ") # Suma 1 para tener posiciones 1-24
        print()
    print()

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
    test_validate_moves(Board(Dice(2, 1)))
    test_validate_moves(Board(Dice(5, 6)))
    test_validate_moves(Board(Dice(6, 3)))
    test_validate_moves(Board(Dice(4, 4)))

    # Bear off normal
    test_validate_moves(Board(Dice(5, 4), 58, [-5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 0, 0))
    
    # Bear off travieso
    test_validate_moves(Board(Dice(4,5), 27, [0, 0, -3, 0, 0, -10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, -2], 0, 0)) 

    # Bear off un movimiento exacto
    test_validate_moves(Board(Dice(6, 2), cells=[0, 0, -2, -4, -4, -3, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 0, 2]))

    # Sin movimientos posibles por bobo
    test_validate_moves(Board(Dice(3,3), cells=[-1, 3, -1, -1, -4, 0, 3, 0, 0, -5, 0, 5, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 4], barB = 1))
    
    # Un solo movimiento con 3 saltos
    test_validate_moves(Board(Dice(4,4), cells=[0, -2, 0, -3, 2, -3, 0, 0, -5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 3, -2, 3, 0, 2, 0]))

    # Sin movimientos posibles porque tiene que sacar de la barra, pero está bloqueada
    test_validate_moves(Board(Dice(6,3), 1, [-2, 0, -2, -2, 0, -5, -2, 0, 0, 0, 0, 0, 0, 0, -1, -1, 4, 0, 9, 0, 0, 0, 1, 0], 1, 0)) 

    # "Treure de barra" amb captura
    board = Board(Dice(5, 2), cells=[-1, -1, 0, -4, -1, -5, 0, 0, 0, 0, 0, 3, 0, 0, -2, 1, 0, 1, 5, 1, 0, 0, 4, 0], barB = 1)
    board = board.flip()
    move = (Move([Jump(-1, 5), Jump(20, 2)]))

    # "Bear off"
    board = Board(Dice(6, 3), cells=[0, -3, -2, 0, 3, -9, 0, -1, 0, 0, 0, 0, 0, 4, 0, 1, 0, 3, 2, 0, 0, 0, 2, 0])
    board = board.flip()
    move = (Move([Jump(16, 6), Jump(21, 3)]))

    # Final de partida amb (-1, 0, .... 0, 1)
    board = Board(Dice(6, 1), cells=[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    board = board.flip()
    move = (Move([Jump(23, 6)]))

    # Comprobar si la partida ha acabat (torn dels negres que han perdut)
    board = Board(Dice(2, 5),turn = 22, cells=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4])
    assert board.over() and board.winner() == 0
    
    # Comprobar si la partida ha acabat (torn dels blanques que han guanyat)
    board = Board(Dice(2, 5),turn = 21, cells=[-4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    assert board.over() and board.winner() == 0