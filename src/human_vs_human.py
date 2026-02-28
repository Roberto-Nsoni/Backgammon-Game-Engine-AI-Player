import sys
from board import Board, WHITE, DiceCup, Move, Jump
from show import show

def read_move(current_board: Board) -> Move:
    """
    Llegeix una linea donada desde la terminal i la converteix en un objecte Move, 
    desprésde validar si aquell moviment era legal.
    Exemple: "0 2 0 1" la converteix Move(jumps=[Jump(point=0, pips=2), Jump(point=0, pips=1)])
    """
    blank_move = Move(jumps=[])

    print("Escriu, per ordre, tots els moviments que vulguis realitzar (point, pip): ")

    while True:
        line = sys.stdin.readline().split()

        # Si l'usuari necessita ajuda per saber els movimients que pot fer
        if line == ["?"]:
            valid_moves = current_board.valid_moves()
            if valid_moves == blank_move:
                print("No tens moviments possibles. Siusplau, passa el torn!")
                continue
            print("Llista de moviments possibles:")
            for index, move in enumerate(valid_moves):
                print(f"{index + 1}: ", end="")
                for jump in move.jumps:
                    print(f"Point: {jump.point + 1} Dice: {jump.pips}\t", end="")
                print() 
            continue
        
        # Si l'usuari no té moviments per fer
        if line == ["\n"]:
            if current_board.valid_moves() == [blank_move]:
                return blank_move
            
        # Si l'entrada no té el el par complet (point, pip)
        if len(line) % 2 != 0:
            print("La entrada no té el parell (point, pip), torna a probar!")
            continue
        
        # Si tot va bé
        move = Move(jumps=[])
        for i in range(0, len(line), 2):
            try:
                point = int(line[i])
                pips = int(line[i+1])
                jump = Jump(point - 1, pips) # Index a la terminal: 1-24, index interns: 0-23
                    
                move.jumps.append(jump)
            except ValueError:
                print("El moviment indicat no està correctament escrit, torna a intetar!")
                continue
        

        if not current_board.is_valid_move(move):
            print("El moviment indicat no es valid, torna a probar!\n(Escriu '?' per veure els moviments possibles)")
        
        else:
            print("Perfecte!")
            return move


def main() -> None:
    """
    Gestiona una partida entre dos persones humans. Representa a la terminal l'estat 
    de cada moviment. Cada torn representa primer el moviment del WHITE i després el moviment del BLACK.
    La partida finalitza quan un dels jugadors guanya la partida.
    """
    # Inicialització de la partida
    seed = 123456
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)

    # Jugar fins que acabi la partida
    # Torn de WHITE
    while not board.over():
        print("Torn del blanc!")
        move = read_move(board)
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)

        # Torn de BLACK
        if not board.over():
            print("Torn del negre!")
            board = board.flip()
            move = read_move(board)
            board = board.play(move)
            board = board.next(cup.roll())
            board = board.flip()
            show(board)

    # Donar els guanyadors i la llavor de la partida
    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()