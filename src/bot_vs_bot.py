from board import Board, DiceCup, WHITE
from show import show
from bot import bot

def main():
    """
    Gestiona una partida entre dos humans. Representa a la terminal l'estat de cada 
    moviment. Cada torn representa primer el moviment del WHITE i després el moviment del BLACK.
    La partida finalitza quan un dels jugadors guanya la partida.
    """
    # Inicialització de la partida
    seed = 123456
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)

    # Jugar fins que acabi la partida
    # Torn del WHITE
    while not board.over():
        print(f"JPetit: \033[3mTinc els daus: {board.dice().die1, board.dice().die2} deixa'm pensar...\033[0m")
        move = bot(board)
        if move.jumps:
            print(f"JPetit: \033[3mCrec que mouré {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}\033[0m")
        else:
            print("JPetit: \033[3mPasso el meu torn, no puc moure fitxes\033[0m (JPetit is sad :c)")
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)

        # Torn del BLACK
        if not board.over():
            board = board.flip()
            print(f"JPetitEvil: \033[3mTinc els daus: {board.dice().die1, board.dice().die2} deixa'm pensar...\033[0m")
            move = bot(board)
            if move.jumps:
                print(f"JPetitEvil: \033[3mCrec que mouré {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}\033[0m")
            else:
                print("JPetitEvil: \033[3mPasso el meu torn, no puc moure fitxes\033[0m (JPetitEvil is turnin' eviler >:c)")
            board = board.play(move)
            board = board.next(cup.roll())
            board = board.flip()
            show(board)
    
    # Donar els guanyadors i la llavor de la partidas
    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()