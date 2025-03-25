import human_vs_human
from board import Board, WHITE, DiceCup, BLACK
from show import show, draw # type: ignore
from bot import bot

def main() -> None:
    """..."""
    seed = 123456
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)
    draw(board, "game.png")
    while not board.over():
        print(seed, board.dice(), board.turn(), board.cells(), board.bar(WHITE), board.bar(BLACK))  
        print("White move?")
        move = human_vs_human.read_move(board)
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)
        draw(board, "game.png")
        
        if not board.over():
            board = board.flip()
            print(f"JPetit: I've got {board.dice().die1, board.dice().die2} let me think...")
            move = bot(board)
            if move.jumps:
                print(f"JPetit: I'm moving {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}")
            else:
                print("JPetit: I skip my turn, I can't move (JPetit is sad :c)")
            board = board.play(move)
            board = board.next(cup.roll())
            board = board.flip()
            show(board)
            draw(board, "game.png")

    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()