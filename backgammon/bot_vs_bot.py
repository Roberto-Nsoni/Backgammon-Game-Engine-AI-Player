from board import Board, DiceCup, WHITE, BLACK
from bot import bot
from show import show, draw # type: ignore

def main():
    seed = 12345
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)

    while not board.over():
        print(seed, board.dice(), board.turn(), board.cells(), board.bar(WHITE), board.bar(BLACK))  
        print(f"JPetit: I've got {board.dice().die1, board.dice().die2} let me think...")
        move = bot(board)
        if move.jumps:
            print(f"JPetit: I'm moving {[(jump.point + 1, jump.pips) for jump in move.jumps]}")
        else:
            print("JPetit: I skip my turn, I can't move (JPetit is sad :c)")
  
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)

        if not board.over():
            print(seed, board.dice(), board.turn(), board.cells(), board.bar(WHITE), board.bar(BLACK))  
            print(f"JPetitEvil: I've got {board.dice().die1, board.dice().die2} let me think...")
            board = board.flip()
            move = bot(board)
            if move.jumps:
                print(f"JPetitEvil: I'm moving {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}")
            else:
                print("JPetitEvil: I skip my turn, I can't move (JPetitEvil is turnin' more evil :c)")
            board = board.play(move)
            board = board.next(cup.roll())
            board = board.flip()
            show(board)
    
    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()