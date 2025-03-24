# arena.py
import random
import uuid
from dataclasses import dataclass, field
from board import Board, WHITE, DiceCup, Move, BLACK, Player

class UserRegistrationError(Exception):
    """Excepció per errors relacionats amb el resgistre d'usuaris."""

class UserLogError(Exception):
    """Excepció per a errors relacionats amb el login/logout dels usuaris."""

class GameError(Exception):
    """Excepció per a errors relacionats amb la gestió interna de les partides."""

@dataclass
class User:
    """Representació d'un usuari a la aplicació."""
    name: str # Nombre real del usuari
    id: str # Sobrenom del usuari, identificador únic
    num_games: int = 0
    num_games_won: int = 0
    list_games: list["Game"] = field(default_factory=list) # Inicialment buida, pero més endavant modificada
    connected: bool = False

    def winrate(self) -> float:
        """Retorna el percentatge de partides guanyades"""
        return round(self.num_games_won / self.num_games * 100, 2) if self.num_games else 0.0

    def in_game(self) -> bool:
        """Retorna 'True' si el jugador es troba actualment en una partida, 
        retorna 'false' alternament"""
        # Comprobar que la última partida estigui acabada
        return bool(self.list_games) and not self.list_games[-1].is_ended()
    
    def add_game(self, game: "Game", won: bool) -> None:
        """Un cop finalitzada la partida, la afegeix a la llista de partides 
        jugades i la contabilitza."""
        self.list_games.append(game)
        self.num_games += 1
        if won:
            self.num_games_won += 1

class Game:
    """Gestiona una partida entre dos usuaris"""
    # Parametres
    _id: str # Identificador únic per la partida
    _user1: User # Jugador WHITE
    _user2: User # Jugador BLACK
    _seed: int # Llavor de la partida que gestiona els daus
    _board: Board # Estat actual del tauler
    _list_moves: list[Move] # Llista de tots els moviments que s'han fet
    _end: bool # "True" si la partida està acabada, "False" alternament
    
    def __init__(self, user1: User, user2: User, seed: int = random.randint(1, 999_999_999),
                 list_moves: list[Move] | None = None, board: Board | None = None) -> None:
        """Inicialitza una nova partida entre dos usuaris, si no es customitza res
        s'utilitzaran valors predeterminats, incloent una llavor aleatòria"""
        self._cup =  DiceCup(seed)
        self._id = str(uuid.uuid4())[:8]
        self._user1 = user1
        self._user2 = user2
        self._seed = seed
        self._list_moves = list_moves if list_moves else []
        self._end = False
        if board:
            self._board = board
        else:
            self._board = Board(DiceCup(seed).roll())
    
    def id(self) -> str:
        """Retorna l'id assossiat a la partida."""
        return self._id
    
    def seed(self) -> int:
        """Retorna la llavor assossiada a la partida"""
        return self._seed
    
    def get_player(self, player: Player) -> User:
        """Retorna l'usuari blanc(WHITE) o negre(BLACK) que està jugant a la partida."""
        return self._user1 if player == WHITE else self._user2

    def is_ended(self) -> bool:
        """Retorna 'True' si la partida ja està acabada, retorna 'False' alternament."""
        return self._end

    def end_game(self) -> None:
        """Canvia l'estat de la partida a 'Finalitzat'"""
        self._end = True
        
    def apply_move(self, move: Move) -> None:
        """Aplica un moviment donat al tauler, tot actualitzant-lo i afeigint aquest 
        moviment a la llista de moviments"""
        self._board = self._board.play(move)
        self._board.next(self._cup.roll())
        self._list_moves.append(move)

class Arena:
    """
    Gestiona l'arena on es juguen les partides, els usuaris registrats, connectats i
    les partides que estiguin actives en aquell moment.
    """
    _reg_users: dict[str, User] # Llista de tots els usuaris registrats. Clau: user.id()
    _con_users: dict[str, User] # Llista de tots els usuaris connectats. Clau: user.id()
    _current_games: dict[str, Game] # Llista de totes les partides que s'estan jugant actualment. Clau: game.id()

    def __init__(self, current_games: dict[str, Game] | None = None,
                reg_users: dict[str, User] | None = None,
                con_users: dict[str, User] | None = None) -> None:
        
        """..."""
        self._reg_users = reg_users if reg_users else {}
        self._con_users = con_users if con_users else {}
        self._current_games = current_games if current_games else {}
    
    def register(self, user: User) -> None:
        """Registra un nou usuari, tot donant-li un identificador únic."""
        if user.id in self._reg_users:
            raise UserRegistrationError("Aquest usuari ja es troba registrat")
        self._reg_users[user.id] = user

    def delete_user(self, user: User) -> None:
        """Dona de baixa un usuari, tot eliminant-lo de la llista d'usuaris."""
        # Assegurar-se de que el jugador s'hagi resitrat primer i que no es trobi en una partida sense acabar
        if user.id not in self._reg_users:
            raise LookupError("Aquest usuari no es troba registrat")
        if user.in_game():
            raise GameError("Aquest jugador es troba actualment en una partida, siusplau esperi a acabar-la abans d'eliminar-lo.")
        
        self._reg_users.pop(user.id)
        if user.id in self._con_users:
            self._con_users.pop(user.id)
        
    def login(self, user: User) -> None:
        "Fa entrar a un usuari (el connecta, fa login) a l'aplicació."
        if user.id not in self._reg_users:
            raise LookupError("Aquest usuari no es troba registrat")
        if user.connected:
            raise UserLogError("Aquest usuari ja es troba connectat")
        
        self._con_users[user.id] = user
        user.connected = True

    def logout(self, user: User) -> None:
        "Fa sortir a un usuari (el desconnecta, fa logout) de l'aplicació."
        if user.id not in self._reg_users:
            raise LookupError("Aquest usuari no es troba registrat")
        if not user.connected:
            raise UserLogError("Aquest usuari ja es troba desconnectat")
        # Si el jugador es troba en partida, es donarà com a "perduda"
        
        if user.in_game():
            last_game = user.list_games[-1]
            self.end_game(last_game.id(), not last_game.get_player(WHITE).id == user.id)
        self._con_users.pop(user.id)
        user.connected = False
    
    def get_reg_players(self) -> list[User]:
        """Retorna una llista de tots els usuaris registrats."""
        return list(self._reg_users.values())
    
    def get_log_players(self) -> list[User]:
        """Obtenir una llista de tots els usuaris connectats."""
        return list(self._con_users.values())

    def get_current_games(self) -> list[Game]:
        """Obtenir una llista de totes les partides actives actualment."""
        return list(self._current_games.values())
    
    def get_player_by_id(self, user_id: str) -> User:
        """Busca un usuari pel seu indentificador."""
        if user_id not in self._reg_users:
            raise LookupError("No hem pogut trobar aquest jugador")

        return self._reg_users[user_id]

    def get_player_by_name(self, name: str) -> User:
        """Busca un usuari pel seu nom de pila. Cal considerar que poden
        haver varies persones amb el mateix nom."""
        for user in self.get_reg_players():
            if user.name == name:
                return user
        
        raise LookupError("Aquest usuari no es troba registrat")
    
    def start_new_game(self, user1: User, user2: User) -> str:
        """Crea una nova partida entre dos usuaris, retorna el ID de la partida.
        Prec: Els dos jugadors han d'estar connectats i cap dels dos ha de tenir una
        partida en curs."""

        # Assrgurar-se que es compleixen les precondicions
        if user1.id == user2.id:
            raise GameError("No pot jugar un usuari contra un mateix!")
        if not (user1.connected or user2.connected):
            raise GameError("Els dos usuaris han d'estar connectats per poder jugar una nova partida!")
        if user1.in_game():
            raise GameError(f'{user1.id} is already playing a game!')
        if user2.in_game():
            raise GameError(f'{user2.id} is already playing a game!')
    
        new_game = Game(user1, user2)
        self._current_games[new_game.id()] = new_game
        
        return new_game.id()
    
    def end_game(self, game_id: str, white_wins: bool) -> None:
        """Fa acabar la partida, contabilitzant la corresponent victòria i derrota al blanc i al negre."""
        if game_id not in self._current_games:
            raise LookupError("Aquest partida no es troba en curs!")
        
        current_game = self._current_games.pop(game_id)
        current_game.end_game()
        user1 = current_game.get_player(WHITE)
        user2 = current_game.get_player(BLACK)
        if white_wins:
            user1.add_game(current_game, True)
            user2.add_game(current_game, False)
        else:
            user1.add_game(current_game, False)
            user2.add_game(current_game, True)
            

    def get_user_games(self, user: User) -> list[Game]:
        """Retorna la llista de totes les partides d'un usuari."""
        if not user.id in self._reg_users:
            raise LookupError("Aquest jugador no es troba registrat!")
        return user.list_games
    
    def get_game(self, user: User, game_id: str) -> tuple[Game, int | None]:
        """Retorna una partida en particular d'un usuari. Si és acabada, també 
        retorna la llavor del gobelet."""

        if user.id not in self._reg_users:
            raise LookupError("Aquest jugador no es troba registrat!")
        for game in user.list_games:
            if game_id == game.id():
                return game, game.seed() if game.is_ended() else None
            
        raise LookupError("La partida no es troba en la llista de partides d'aquest jugador!")
    
    def get_ranking(self) -> list[User]:
        """Retorna la classificació dels usuaris, ordenats per percentatge de partides guanyades."""
        return sorted(self._reg_users.values(), key=lambda x: x.winrate(), reverse=True)

def main() -> None:
    """Funció principial que permet navegar ente les diferents opcions de l'arena"""
    arena = Arena()
    while True:
        print("\n--- Menú ---")
        print("0. Sortir")
        print("1. Registrar usuari")
        print("2. Iniciar sessió")
        print("3. Tancar sesió")
        print("4. Eliminar usuari")
        print("5. Crear partida")
        print("6. Veure usuaris registrats")
        print("7. Veure usuaris connectats")
        print("8. Veure partides en curs")
        print("9. Veure partides d'un jugador")
        print("10. Veure ranking de jugadors")
        
        option = input("Selecciona una opció: ")

        if option == "0":
            print("Sortint de l'aplicació...")
            break
        
        if option == "1":
            nom = input("Nom: ")
            user_id = input("ID Usuari: ")
            user = User(nom, user_id)
            
            try:
                arena.register(user)
                print(f"Usuari {user_id} registrat correctament.")
            except UserRegistrationError as e:
                print(e)
        
        elif option == "2":
            user_id = input("ID usuari: ")
            try:
                arena.login(arena.get_player_by_id(user_id))
                print(f"{user_id} ha iniciat sessió.")
            except (LookupError, UserLogError) as e:
                print(e)
        
        elif option == "3":
            user_id = input("ID Usuari: ")
            try:
                arena.logout(arena.get_player_by_name(user_id))
                print(f"{user_id} ha tancat sessió.")
            except (LookupError, UserLogError) as e:
                print(e)


        elif option == "4":
            user_id = input("ID Usuari: ")
            try:
                arena.delete_user(arena.get_player_by_name(user_id))
                print(f"Usuari {user_id} eliminat correctament.")
            except (LookupError, GameError) as e:
                print(f"Error: {e}")

        elif option == "5":
            print("Crear partida:")
            user_id1 = input("ID Usuari del jugador WHITE: ")
            user_id2 = input("ID Usuari del jugador BLACK: ")
            try:
                user1 = arena.get_player_by_name(user_id1)
                user2 = arena.get_player_by_name(user_id2)
                game_id = arena.start_new_game(user1, user2)
                print(f"Partida creada correctament amb ID: {game_id}")
            except GameError as e:
                print(f"Error: {e}")

        elif option == "6":
            print("Usuaris registrats:")
            for user in arena.get_reg_players():
                print(user)
                # print(f"Nickname: {user.id}, Nom: {user.name}, Winrate: {user.winrate()}%")
        
        elif option == "7":
            print("Usuaris connectats:")
            for user in arena.get_log_players():
                print(user)
                # print(f"Nickname: {user.id}, Nom: {user.name}")
        
        elif option == "8":
            print("Partides en curs:")
            current_games = arena.get_current_games()
            if current_games:
                for game in current_games:
                    white = game.get_player(WHITE).id
                    black = game.get_player(BLACK).id
                    print(f"ID: {game.id()} - WHITE: {white} V.S. BLACK: {black}")
            else:
                print("No hi ha partides en curs.")
        
        elif option == "9":
            user_id = input("ID Usuari: ")
            game_id = input("ID Partida: ")
            try:
                game = arena.get_game(arena.get_player_by_id(user_id), game_id)
                print(game)
            except LookupError as e:
                print(f"Error: {e}")

        elif option == "10":
            print("Ranking de jugadors:")
            ranking = arena.get_ranking()
            for i, user in enumerate(ranking):
                print(f'{i} - {user}')
                # print(f"{i}. {user.id} - Winrate: {user.winrate()}%")
    
        else:
            print("Opció no vàlida, siusplau trii una opció del 0 al 10.")

if __name__ == "__main__":
    main()
