from board import Board, WHITE, DiceCup, Move, Jump
from show import show
import sys

def read_move(current_board: Board) -> Move:
    """
    Llegeix una linea donada desde la terminal i la converteix en un objecte Move, 
    desprésde validar si aquell moviment era legal.
    Exemple: "0 2 0 1" la converteix Move(jumps=[Jump(point=0, pips=2), Jump(point=0, pips=1)])
    """

    while True:
        line = sys.stdin.readline().split()
        # Error la entrada no té el el par complet (point, pip)
        if len(line) % 2 != 0:
            print("La entrada no té el parell (point, pip), torna a probar!")
            continue
        move = Move(jumps=[])
        for i in range(0, len(line), 2):
            try:
                point = int(line[i])
                pips = int(line[i+1])
                if current_board.current() == WHITE:
                    jump = Jump(point - 1, pips) # Index a la terminal: 1-24, index interns: 0-23
                else:
                    jump = Jump(23 - point + 1, pips) # Index a la terminal: 24-1, index interns: 0-23
                    
                move.jumps.append(jump)
            except ValueError:
                print("El moviment indicat no està correctament escrit, torna a intetar!")
                continue
        
        if not current_board.is_valid_move(move):
            print("El moviment indicat no es valid, torna a probar!", move)
            for i in current_board.valid_moves():
                print(i)
        
        else:
            return move


def main() -> None:
    """..."""

    seed = 123456
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)
    while not board.over():
        print("White move?")
        move = read_move(board)
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)
        if not board.over():
            print("Black move?")
            move = read_move(board)
            board = board.play(move)
            board = board.next(cup.roll())
            show(board)
    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()