import human_vs_human
from board import Board, WHITE, DiceCup, BLACK
from show import show
from bot import bot

def main() -> None:
    """
    Gestiona una partida entre un humà i un bot. Representa a la terminal l'estat 
    de cada moviment. Cada torn representa: primer el moviment del WHITE(l'humà) 
    i després el moviment del BLACK(el bot).
    La partida finalitza quan un dels jugadors guanya la partida.
    """
    # Inicialització de la partida
    seed = 123456
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)

    # Jugar fins que acabi la partida
    # Torn de l'humà
    while not board.over():
        print(seed, board.dice(), board.turn(), board.cells(), board.bar(WHITE), board.bar(BLACK))  
        print("White move?")
        move = human_vs_human.read_move(board)
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)
        
        # Torn del bot
        if not board.over():
            board = board.flip()
            print(f"JPetit: \033[3mI've got {board.dice().die1, board.dice().die2} let me think...\033[0m")
            move = bot(board)
            if move.jumps:
                print(f"JPetit: \033[3mI'm moving {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}\033[0m")
            else:
                print("JPetit: \033[3mI skip my turn, I can't move\033[0m (JPetit is sad :c)")
            board = board.play(move)
            board = board.next(cup.roll())
            board = board.flip()
            show(board)

    # Donar els guanyadors i la llavor de la partida
    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()