from board import Board, Dice, DiceCup, WHITE, BLACK # type: ignore ##################
from bot import bot
from show import show

def main():
    seed = 498232
    cup = DiceCup(seed)
    board = Board(cup.roll())
    show(board)
    while not board.over():
        print(f"JPetit: I've got {board.dice().die1, board.dice().die2} let me think...")
        move = bot(board)
        if move.jumps:
            print(f"JPetit: I'm moving {[(jump.point + 1, jump.pips) for jump in move.jumps]}")
        else:
            print(f"JPetit: I skip my turn, I can't move (JPetit is sad :c)")
        board = board.play(move)
        board = board.next(cup.roll())
        show(board)

        if not board.over():
            print(f"JPetitEvil: I've got {board.dice().die1, board.dice().die2} let me think...")
            move = bot(board)
            if move.jumps:
                print(f"JPetitEvil: I'm moving {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}")
            else:
                print(f"JPetitEvil: I skip my turn, I can't move (JPetitEvil if turnin' more evil :c)")
            
            board = board.play(move)
            board = board.next(cup.roll())
            show(board)
    
    print(board.winner())
    print(f"Winner: {'W' if board.winner() == WHITE else 'B'}")
    print(f"Seed: {seed}")

if __name__ == "__main__":
    main()