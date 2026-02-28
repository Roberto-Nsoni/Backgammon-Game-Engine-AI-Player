import random, uuid, pickle
from dataclasses import dataclass, field

import human_vs_human, bot
from board import Board, WHITE, DiceCup, Move
from show import show

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
        return bool(self.list_games) and not self.list_games[-1].end
    
    def add_new_game(self, game: "Game") -> None:
        """Afegeix un nou joc a la llista de partides jugades"""
        self.list_games.append(game)
        self.num_games += 1

@dataclass
class Game:
    """
    Gestiona una partida entre dos usuaris. Si no es customitza res
       s'inicialitza amb els valors predeterminats d'una nova partida, 
       incloent una llavor aleatòria.
       """
    id = str(uuid.uuid4())[:8] # Identifiacdon únic per la partida
    user1: User # Jugador WHITE
    user2: User # Jugador BLACK
    seed: int = random.randint(1, 999_999_999) # Llavor de la partida que gestiona els daus
    cup: DiceCup =  DiceCup(seed)
    board: Board = Board(DiceCup(seed).roll()) # Estat actual del tauler
    list_moves: list[Move] = field(default_factory=list) # Llista de tots els moviments que s'han fet
    end: bool = False # "True" si la partida està acabada, "False" alternament
        
    def apply_move(self, move: Move) -> None:
        """
        Aplica un moviment donat al tauler, tot actualitzant-lo i afeigint aquest 
        moviment a la llista de moviments.
        """
        self.board = self.board.play(move)
        self.board = self.board.next(self.cup.roll())
        self.list_moves.append(move)

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
        
        """Constructor del programa."""
        # La configuració "default" crea a aquest usuari com el bot
        bot = User("Jordi Petit", "JPetit", connected=True)
        self._reg_users = reg_users if reg_users is not None else {bot.id: bot}
        self._con_users = con_users if con_users is not None else {bot.id: bot}
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

    def login(self, user: User) -> None:
        """Fa entrar a un usuari (el connecta, fa login) a l'aplicació."""
        if user.id not in self._reg_users:
            raise LookupError("Aquest usuari no es troba registrat")
        if user.connected:
            raise UserLogError("Aquest usuari ja es troba connectat")
        
        self._con_users[user.id] = user
        user.connected = True

    def logout(self, user: User) -> None:
        """Fa sortir a un usuari (el desconnecta, fa logout) de l'aplicació."""
        if user.id not in self._reg_users:
            raise LookupError("Aquest usuari no es troba registrat")
        if not user.connected:
            raise UserLogError("Aquest usuari ja es troba desconnectat")
        if user.in_game():
            raise GameError("Aquest jugador es troba actualment en una partida, siusplau esperi a acabar-la abans d'eliminar-lo.")
        
        self._con_users.pop(user.id)
        user.connected = False
    
    def get_reg_users(self) -> list[User]:
        """Retorna una llista de tots els usuaris registrats."""
        return list(self._reg_users.values())
    
    def get_log_users(self) -> list[User]:
        """Obtenir una llista de tots els usuaris connectats."""
        return list(self._con_users.values())

    def get_current_games(self) -> list[Game]:
        """Obtenir una llista de totes les partides actives actualment."""
        return list(self._current_games.values())
    
    def get_user_by_id(self, user_id: str) -> User:
        """Busca un usuari pel seu indentificador."""
        if user_id not in self._reg_users:
            raise LookupError("No hem pogut trobar aquest jugador")

        return self._reg_users[user_id]

    def get_user_by_name(self, name: str) -> list[User]:
        """
        Busca un usuari pel seu nom de pila. Cal considerar que poden
        haver varies persones amb el mateix nom.
        """
        users: list[User] = []
        for user in self.get_reg_users():
            if user.name == name:
                users.append(user)
        if not users:
            raise LookupError("Aquest usuari no es troba registrat")
        return users
    
    def start_new_game(self, user1: User, user2: User) -> Game:
        """
        Crea una nova partida entre dos usuaris, retorna el ID de la partida.
        Si l'usuari2 és JPetit es considerarà que juga un humà contra un bot
        Prec: Els dos jugadors han d'estar connectats i cap dels dos ha de tenir una
        partida en curs.
        """
        # Assrgurar-se que es compleixen les precondicions
        if user1.id == user2.id:
            raise GameError("No pot jugar un usuari contra un mateix!")
        if not (user1.connected and user2.connected):
            raise GameError("Els dos usuaris han d'estar connectats per poder jugar una nova partida!")
        if user1.in_game():
            raise GameError(f'{user1.id} ja té en una partida en curs!')
        if user2.id != "JPetit" and user2.in_game():
            raise GameError(f'{user2.id} ja té en una partida en curs')
        
        game = Game(user1, user2)
        
        # Actualitzar correctament tota la informació
        self._current_games[game.id] = game
        user1.add_new_game(game)
        user2.add_new_game(game)
        return game
    
    def play(self, game: Game) -> None: # pragma: no cover (no fa falta fer tests per comprobar que funciona)
        """Realitza una partida entre dos usuaris, si l'usuari BLACK és
        el bot, juga el bot al torn de BLACK"""

        show(game.board)
        # Es juga fins que hi hagi un guanyador
        while not game.board.over():
            print("Torn del blanc!")
            move = human_vs_human.read_move(game.board)
            game.apply_move(move)
            show(game.board)
            if not game.board.over():          
                game.board = game.board.flip()
                if game.user2.id == "JPetit":
                    print(f"JPetit: \033[3mTinc els daus: {game.board.dice().die1, game.board.dice().die2} deixa'm pensar...\033[0m")
                    move = bot.bot(game.board)
                    if move.jumps:
                        print(f"JPetit: \033[3mCrec que mouré {[(23 - jump.point + 1, jump.pips) for jump in move.jumps]}\033[0m")
                    else:
                        print("JPetit: \033[3mPasso el meu torn, no puc moure fitxes\033[0m (JPetit is sad :c)")
                else:
                    print("Torn del negre!")
                    move = human_vs_human.read_move(game.board)
                game.apply_move(move)
                game.board = game.board.flip()
                show(game.board)
        
        # Un cop finalitza la partida es dona al guanyador
        winner = "W" if game.board.winner() == WHITE else "B"
        print(f"Guanyador: {winner}")
        print(f"Moviments realitzats en aquesta partida: {game.list_moves}")
        self.end_game(game.id, game.board.winner() == WHITE)

    def end_game(self, game_id: str, white_wins: bool) -> None:
        """Fa acabar la partida, contabilitzant la corresponent victòria 
        i derrota al blanc o al negre."""
        if game_id not in self._current_games:
            raise LookupError("Aquest partida no es troba en curs!")
        
        current_game = self._current_games.pop(game_id)
        current_game.end = True
        user1 = current_game.user1
        user2 = current_game.user2
        if white_wins:
            user1.num_games_won += 1
        else:
            user2.num_games_won += 1
            

    def get_user_games(self, user: User) -> list[Game]:
        """Retorna la llista de totes les partides d'un usuari."""
        if not user.id in self._reg_users:
            raise LookupError("Aquest jugador no es troba registrat!")
        return user.list_games
    
    def get_game(self, user_id: str, game_id: str) -> tuple[Game, int | None]:
        """Retorna una partida en particular d'un usuari. Si és acabada, també 
        retorna la llavor del gobelet."""

        if user_id not in self._reg_users:
            raise LookupError("Aquest jugador no es troba registrat!")
        for game in self.get_user_by_id(user_id).list_games:
            if game_id == game.id:
                return game, game.seed if game.end else None
            
        raise LookupError("La partida no es troba en la llista de partides d'aquest jugador!")
    
    def get_ranking(self) -> list[User]:
        """Retorna la classificació dels usuaris, ordenats per percentatge de partides guanyades."""
        return sorted(self._reg_users.values(), key=lambda x: x.winrate(), reverse=True)

def main(arena: Arena) -> None: # pragma: no cover (no fa falta comprobar amb tests si funciona, té més sentit provar-ho)
    """Funció principial que permet navegar ente les diferents opcions de l'arena"""
    
    logged_in, logged_id = False, None
    while True:
        print("\n---- Benvingut al servidor de Backgammon! ----")
        print("0. Sortir")
        print("1. Registrar usuari")
        print("2. Iniciar sessió")
        
        option = input("Selecciona una opció: ")

        # Sortir del menú
        if option == "0":
            print("\nSortint...")
            break

        # Registrar un nou usuari
        if option == "1":
            nom = input("\nNom: ")
            user_id = input("ID Usuari: ")
            user = User(nom, user_id)
            try:
                arena.register(user)
                print(f"\nUsuari {user_id} registrat correctament.")
            except UserRegistrationError as e:
                print(f"\nError: {e}")

        # Iniciar sessió com a usuari
        elif option == "2":
            user_id = input("\nID usuari: ")
            try:
                arena.login(arena.get_user_by_id(user_id))
                print(f"\n{user_id} ha iniciat sessió.")
                logged_in = True
                logged_id = user_id
            except (LookupError, UserLogError) as e:
                print(f"\nError: {e}")
        else:
            print("\nOpció no vàlida, torna a probar!")

        # Un cop la sessió està iniciada, ja es poden fer moltes més coses
        while logged_in and logged_id:
            print(f"\n---- Benvingut {logged_id}! ----")        
            print("\n0. Tancar sessió")
            print("1. Eliminar usuari")
            print("2. Jugar partida")
            print("3. Veure usuaris registrats")
            print("4. Veure partides en curs")
            print("5. Veure detalls del perfil d'un usuari")
            print("6. Veure partides d'un jugador")
            print("7. Veure ranking de jugadors")

            option = input("\nSelecciona una opció: ")

            # Tancar la sessió i tornar al menú principal
            if option == "0":
                try:
                    arena.logout(arena.get_user_by_id(logged_id))
                    print(f"\n{logged_id} ha tancat sessió.")
                    logged_in = False
                    break
                except (LookupError, UserLogError) as e:
                    print(e)

            # Eliminar l'usuari i tornar al menú principal
            if option == "1":
                confirmation = input("\nEstàs segur que vols eliminar aquest usuari?\n"
                "Aquesta acció és irrecuperable!"
                "(y/n): ")
                if confirmation == "y":
                    try:
                        arena.delete_user(arena.get_user_by_id(logged_id))
                        print(f"\nUsuari {logged_id} eliminat correctament.")
                        logged_in = False
                        break
                    except (LookupError, GameError) as e:
                        print(f"\nError: {e}")

            # Jugar una nova partida
            if option == "2":
                while True:  
                    print("\nJugar partida")
                    print("0 Tornar al menú principal")
                    print("1 Jugar partida humà contra humà.")
                    print("2 Jugar partida humà contra bot.")

                    option = input("\nSeleccioni una opció: ")

                    user1 = arena.get_user_by_id(logged_id)

                    if option == "0":
                        break
                    if option == "1":
                        user_id2 = input("\nID Usuari del jugador contra qui vulguis jugar: ")
                    elif option == "2":
                        user_id2 = "JPetit"
                    else:
                        print("\nOpció no válida. Torna a probar!")
                        continue
                    try:
                        user2 = arena.get_user_by_id(user_id2)
                        game = arena.start_new_game(user1, user2)
                        print(f"\nPartida creada correctament amb ID: {game.id}\n") 
                        arena.play(game)
                    except GameError as e:
                        print(f"\nError: {e}")

            # Veure una llista dels usuaris registrats
            elif option == "3":
                print("\nUsuaris registrats:")
                for i, user in enumerate(arena.get_reg_users()):
                    print(f"{i}. {user.id} ({user.name}) - Connectat: {user.connected}")
            
            # Veure una llista de totes les partides en curs a l'Arena
            elif option == "4":
                print("\nPartides en curs:")
                current_games = arena.get_current_games()
                if current_games:
                    for game in current_games:
                        white = game.user1.id
                        black = game.user2.id
                        print(f"\nID Partida: {game.id} - WHITE: {white} VS. BLACK: {black}")
                else:
                    print("\nNo hi ha partides en curs.")

            # Veure el perfil detallat d'un usuari
            elif option == "5":
                user_id2 = input("\nID Usuari: ")
                try:
                    user = arena.get_user_by_id(user_id2)
                    print(f"\nDetalls de {user_id2}:\n{user}")
                except LookupError as e:
                    print(e)
            
            # Veure els detalls d'una partida d'un usuari
            elif option == "6":
                user_id = input("\nID Usuari: ")
                game_id = input("ID Partida: ")
                try:
                    game, seed = arena.get_game(user_id, game_id)

                    # Si la partida ha finalitzat, cal retornar també la llavor
                    if seed:
                        print(f"Partida finalitzada amb la llavor: {seed}")
                    print(game)

                except LookupError as e:
                    print(f"\nError: {e}")

            # Veure el ranking dels jugadors
            elif option == "7":
                print("\nRanking de jugadors:")
                ranking = arena.get_ranking()
                for i, user in enumerate(ranking):
                    print(f"{i}. {user.id} - Winrate: {user.winrate()}%")       
            else:
                print("\nOpció no vàlida, torna a probar!")
    
    # Quan es vol sortir del menú, guardem les dades de l'arena
    with open("arena-data.dat", "wb") as file:
        pickle.dump(arena, file)

if __name__ == "__main__": # pragma: no cover (no fa falta fer tests en aquesta part)
    try:
        with open("arena-data.dat", "rb") as file:
            arena = pickle.load(file)
            print("Dades de l'arena carregades correctament")
    except FileNotFoundError:
        arena = Arena()
        print("Nova arena creada correctament")
    
    main(arena)