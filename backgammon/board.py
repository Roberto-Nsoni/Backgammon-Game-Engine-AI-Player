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
        return Dice(self._next() % 6 + 1, self._next() % 6 + 1)

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
        """..."""
        self._dice = dice.copy()
        self._barW = barW
        self._barB = barB
        self._turn = turn
        self._offW = 0
        self._offB = 0

        # Generació de les caselles
        if cells:
            self._cells = cells
        else:
            self._cells = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2] # Tauler amb les posicions inicials
        
    def copy(self) -> Board:
        """Retorna una copia del tauler actual."""
        return Board(self.dice(), self.turn(), self.cells(), self.bar(WHITE), self.bar(BLACK))

    def flip(self) -> Board:
        """Retorna el mateix tauler amb els colors i sentits invertits."""
        return Board(self.dice(), self.turn(), [-i for i in self.cells()], self.bar(BLACK), self.bar(WHITE))

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
            return WHITE
        elif self.off(BLACK) == 15:
            return BLACK    
        else:
            return None

    def over(self) -> bool:
        """Retorna "True" si la partida ha acabat, retorna "False" alternament."""
        return not (self.winner() == None)

    def valid_moves(self) -> list[Move]:
        """..."""
        ...

    def is_valid_move(self, move: Move) -> bool:
        """..."""
        ...

    def play(self, move: Move) -> Board:
        """..."""
        ...
        
    def next(self, dice: Dice) -> Board:
        """..."""
        ...
