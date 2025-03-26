from board import Board, Move, WHITE
from dataclasses import dataclass


@dataclass
class EvaluatedMove:
    move: Move
    score: int

def bot(board: Board) -> Move:
    """
    Escull la millor jugada possible pel jugador actual, suposant que el rival jugarà 
    la miilor resposta a aquell moviment.    
    """
    moves = evaluate_moves(board)
    # Si hi han moviments possibles, retorna el de millor puntuació, sino retorna buit.
    return moves[0].move if moves else Move(jumps=[])

def evaluate_moves(board: Board) -> list[EvaluatedMove]:
    """Donat un tauler, retorna una llista ordenada de les millors jugades possibles."""
    evaluated_moves: list[EvaluatedMove] = []

    # Evalua tots els possibles moviments del blanc
    white_moves = [EvaluatedMove(move, evaluate_board(board, move)) for move in board.valid_moves()]

    white_moves.sort(key=lambda x: (x.score), reverse=True)
    
    # Por cada moviment que pot fer el blanc, suposem que el negre jugarà la millor resposta
    for white_move in white_moves[:50]:
        simulated_board = board.copy().play(white_move.move)

        # Trobar la millor resposta del negre
        best_Bmove = 0
        for Bmove in simulated_board.valid_moves():
            board_puntuation = evaluate_board(simulated_board, Bmove)
            best_Bmove = max(best_Bmove, board_puntuation)
        
        # L'evaluació serà la diferència entre el moviment del blanc i la del negre
        evaluated_moves.append(EvaluatedMove(white_move.move, white_move.score - best_Bmove))
    
    # Ordenem els moviments per puntuació de major a menor
    return (sorted(evaluated_moves, key=lambda x: (x.score), reverse=True))
        

def evaluate_board(board: Board, move: Move) -> int:
    """
    Coses a tenir en compte:
    1) Quan més avançades les fitxes millor (cada posició +1)
    2) Fer "bear off" (cada fitxa +50)
    3) Tenir fitxes a la barra (-25 per fitxa)
    4) Tenir fitxes soles (cada fitxa -5)
    """
    move_puntuation = 0
    next_board = board.copy().play(move)

    # Quan més avançades les fitxes millor (cada posició +1)
    for cell in next_board.cells():
        if cell >= 1:
            move_puntuation += cell

    # Fer "bear off" (cada fitxa +30)
    move_puntuation += 30 * next_board.off(WHITE)

    # Tenir fitxes a la barra (-20 punts per fitxa)
    move_puntuation -= 20 * next_board.bar(WHITE)

    # Tenir fitxes soles (cada fitxa -15)
    for cell in next_board.cells():
        if cell == 1:
            move_puntuation -= 15
    
    return move_puntuation