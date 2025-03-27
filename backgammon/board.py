from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


WHITE = 0
BLACK = 1
BAR = -1


type Player = Literal[0] | Literal[1]
type OptionalPlayer = Player | None


@dataclass
class Dice:

    die1: int  # 1..6
    die2: int  # 1..6

    def copy(self) -> Dice:
        return Dice(self.die1, self.die2)

    def is_double(self) -> bool:
        return self.die1 == self.die2

    def is_valid(self) -> bool:
        return 1 <= self.die1 <= 6 and 1 <= self.die2 <= 6


class DiceCup:

    _a = 1664525
    _c = 1013904223
    _m = 2**32
    _seed: int

    def __init__(self, seed: int):
        self._seed = seed

    def roll(self) -> Dice:
        return Dice((self._next() % 1009) % 6 + 1, (self._next() % 1009) % 6 + 1)

    def _next(self) -> int:
        self._seed = (self._a * self._seed + self._c) % self._m
        return self._seed


@dataclass
class Jump:

    point: int  # 0..23 | -1 (bar)
    pips: int  # 1..6


@dataclass
class Move:

    jumps: list[Jump]  # length 0-4


class Board:

    # Parameters:
    
    _dice: Dice # Daus que han sortit per la jugada actual
    _barW: int # Nombre de fitxes blanques a la barra
    _barB: int # Nombre de fitxes negres a la barra
    _turn: int # Torn actual de la partida
    _cells: list[int] # Nombre de fitxes, per posició, al tauler
    _offW: int # Nombre de fitxes que han salvat les blanques
    _offB: int # Nombre de fitxes que han salvat les negres

    def __init__(self, dice: Dice, turn: int = 1, cells: list[int] | None = None, barW: int = 0, barB: int = 0) -> None:
        """Construcció inicial del tauler, si no es personalitza res, es tracta com una nova partida."""
        self._dice = dice.copy()
        self._barW = barW
        self._barB = barB
        self._turn = turn

        # Generació de les caselles
        if cells:
            self._cells = cells
        else:
            self._cells = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2] # Tauler amb les posicions inicials
        
        self._offW = 15 - sum([cell for cell in self._cells if cell > 0]) - self._barW # Totes les blanques que NO hi són al tauler
        self._offB = 15 + sum([cell for cell in self._cells if cell < 0]) - self._barB # Totes les fixtes negres que NO ho son al tauler
        
    def copy(self) -> Board:
        """Retorna una copia del tauler actual."""
        return Board(self.dice(), self.turn(), self.cells(), self.bar(WHITE), self.bar(BLACK))

    def flip(self) -> Board:
        """Retorna el mateix tauler amb els colors i sentits invertits."""
        return Board(self.dice(), self.turn(), list(reversed([-i for i in self.cells()])), self.bar(BLACK), self.bar(WHITE))

    def cells(self) -> list[int]:
        """Retorna una llista amb el nombre de fitxes, per posicions, al tauler"""
        return self._cells.copy()

    def cell(self, i: int) -> int:
        """Retorna el nombre de fitxes que hi ha a una posició concreta del tauler.
        Prec: 0 <= i <= 23"""
        return self._cells[i]

    def bar(self, player: Player) -> int:
        """Retorna el nombre de fitxes que té a la barra el jugador (blanc o negre)"""
        return self._barW if player == WHITE else self._barB

    def off(self, player: Player) -> int:
        """Retorna el nombre de fitxes que té salvades el jugador (blanc o negre)"""
        return self._offW if player == WHITE else self._offB

    def dice(self) -> Dice:
        """Retorna una copia del dau actual que s'està jugant"""
        return self._dice

    def turn(self) -> int:
        """Retorna el torn actual que s'està jugant"""
        return self._turn

    def current(self) -> OptionalPlayer:
        """Retorna el jugador que li toca moure al torn actual"""
        if self._turn % 2 == 1:
            return WHITE
        else:
            return BLACK

    def winner(self) -> OptionalPlayer:
        """Retorna el jugador que ha guanyat la partida (si encara no ha acabat, retorna None)"""
        if self.off(WHITE) == 15:
            return WHITE if self.current() == WHITE else BLACK
        if self.off(BLACK) == 15:
            return BLACK if self.current() == WHITE else WHITE
        return None

    def over(self) -> bool:
        """Retorna 'True' si la partida ha acabat, retorna "False" alternament."""
        return not self.winner() is None

    def valid_moves(self) -> list[Move]:
        """Retorna una llista amb tots els possibles moviments válids que es poden fer"""
        # Comprobar si la jugada té dobles
        if self.dice().is_double():
            list_dice = [self.dice().die1]*2 + [self.dice().die2]*2
        else:
            list_dice = [self.dice().die1, self.dice().die2]

        # Generar tots els possibles moviments que es poden fer
        possible_moves = self._generate_moves(self.copy(), list_dice, [])

        # Quedar-se només amb aquells que tinguin el màxim nombre de moviments
        if possible_moves:
            len_moves = max(len(move.jumps) for move in possible_moves)

            # Si el moviment només té un salt, cal utilitzar el dau més gran
            if len_moves == 1:
                max_move = max((move.jumps[0].pips for move in possible_moves if move.jumps))
                valid_moves = [move for move in possible_moves if (move.jumps and move.jumps[0].pips == max_move)]
            else:
                valid_moves = [move for move in possible_moves if len(move.jumps) == len_moves]
        else:
            valid_moves = []

        return valid_moves
      
    def is_valid_move(self, move: Move) -> bool:
        """
        Donat un moviment, retorna 'True' si aquest és vàlid, considerant l'estat
        actual del tauler. Retorn 'False' alternament.
        """
        return move in self.valid_moves()

    def play(self, move: Move) -> Board:
        """
        Retorna una copia del tauler després d'aplicar-li un moviment.
        Prec: El moviment ha de ser vàlid.
        """
        next_board = self.copy()
        for jump in move.jumps:
            jump_position = jump.point + jump.pips

            # Treure la fitxa de l'origen
            if jump.point == -1:
                next_board._barW -= 1
            else:
                next_board._cells[jump.point] -= 1

            # Si el moviment es un "bear off"
            if jump_position > 23:
                next_board._offW += 1

            # Si el moviment és una captura
            elif next_board.cell(jump_position) == -1:
                next_board._cells[jump_position] = 1
                next_board._barB += 1

            # Si és un moviment normal
            else:
                next_board._cells[jump_position] += 1

        return next_board
        
    def next(self, dice: Dice) -> Board:
        """Retorna una copia del tauler preparat pel següent moviment."""
        next_board = self.copy()
        next_board._dice = dice
        next_board._turn += 1
        return next_board
    
    def _generate_moves(self, current_board: Board, list_dice: list[int], list_moves: list[Move] = [], current_move: Move = Move(jumps=[])) -> list[Move]:
        """
        Donat un tauler i una llista de daus, utilitza generació exhaustiva per retornar una llista amb 
        tots els possibles moviments que es poden fer.
        Nota: Cal diferenciar entre salts (moure una fitxa x posicions) de moviments (moure x fitxes y posicions)
        """
        # Cas base: No tenim daus disponibles, per tant, no podem fer salts xd
        if list_dice == []:
            list_moves.append(current_move)
            return list_moves
        
        else:
            # Per cada dau que encara ens quedi, generem tots els salts válids que podem fer
            valid_jumps: list[Jump] | None = []
            for die in list_dice:
                valid_jumps = self._generate_jumps(current_board, die)

                # Si tenim salts válids, per cadascun generem recursivament els moviments següents
                if valid_jumps:
                    for jump in valid_jumps:
                        # Modificar el tauler i el moviment per simular el salt.
                        new_board = current_board.copy().play(Move(jumps=[jump]))
                        new_current_move = Move(jumps=current_move.jumps + [jump])

                        new_list_dice = list_dice[:]
                        new_list_dice.remove(die)

                        # Recursió per generar més moviments a partir del salt
                        self._generate_moves(new_board, new_list_dice, list_moves, new_current_move)

                # Si resulta que els daus són dobles, no cal provar per tots els daus restants, ja que són iguals
                if current_board.dice().is_double():
                    list_moves.append(current_move)
                    return list_moves
            
            # Si després de probar amb tots els daus no podem fer salts, afeigim el moviment que haguem fet fins aquest
            if not valid_jumps:
                list_moves.append(current_move) 

            return list_moves
        
    def _generate_jumps(self, board: Board, die: int) -> list[Jump] | None:
        """
        Donat un tauler i un moviment de dau, retorna tots els salts legals que es poden
        fer en aquella jugada.
        """
        list_jumps: list[Jump] = []

        # Per fitxes a la barra
        if board.bar(WHITE) > 0:    
            next_position = die - 1
            next_position_points = board.cell(next_position)
            
            # Si a la següent posició tenim ALGUNA fitxa blanca, EXACTAMENT UNA negra o ESTA BUIDA, el moviment és legal
            if next_position_points >= -1:
                list_jumps.append(Jump(-1, die))
                return list_jumps
            return None

        # Per fitxes al tauler
        for position, points in enumerate(board.cells()): # position: nombre casella, points: fitxes a la casella
            # Si la casella pertany al jugador blanc
            if points >= 1: 
                next_position = position + die
                # Si el moviment és un "bear off" válid
                if next_position > 23:
                    if self._can_bear_off(board, Jump(position, die)):
                        list_jumps.append(Jump(position, die))

                else:
                    next_position_points = board.cell(next_position)
                    # Si a la següent posició tenim ALGUNA fitxa blanca, EXACTAMENT UNA negra o ESTA BUIDA, el moviment és legal
                    if next_position_points >= -1:
                        list_jumps.append(Jump(position, die))                
        return list_jumps
    
    def _can_bear_off(self, board: Board, jump: Jump) -> bool:
        """
        Donat un tauler, retorna "True" si totes les fitxes blanques es troben al home 
        per fer "bear off". Retorna "False" alternament.
        """
        # Assegurar-se de que no hi ha cap fitxa fora del home board, sino pot fer "bear off".
        for position, points in enumerate(board.cells()): # position: nombre casella, points: fitxes a la casella
            if points >= 1 and position < 18:
                return False
            if position >= 18:
                break
    
        # Si el salt es "exacte"
        if jump.point + jump.pips == 24:
            return True

        # Si el salt es passa
        furthest_point = min((pos for pos in range(18, 24) if (board.cell(pos) >= 1 and pos + max(self.dice().die1, self.dice().die2) >= 24)))
        if jump.point + jump.pips > 24 and jump.point == furthest_point:
            return True
        
        return False

