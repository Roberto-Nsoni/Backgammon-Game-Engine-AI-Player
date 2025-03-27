import pytest
from arena import User, Arena, UserRegistrationError, UserLogError, GameError

def test_apply_move():
    arena = Arena(reg_users={}, con_users={}, current_games={})
    user1 = User("Test1", "test1")
    user2 = User("Test2", "test2")
    arena.register(user1)
    arena.register(user2)
    arena.login(user1)
    arena.login(user2)
    game = arena.start_new_game(user1, user2)
    game.seed = 123456
    move = game.board.valid_moves()[0]
    # Aplicar movmient i comprobar que s'actualitza correctament
    game.apply_move(move)
    assert move in game.list_moves
    
def test_user_related() -> None:
    # Inicialitzem una arena buida
    arena = Arena(reg_users={}, con_users={}, current_games={})

    # Creem dos usuaris amb el mateix nom, pero ID diferent
    user1 = User("UserBot", "test1")
    user2 = User("UserBot", "test2")

    # --- Register ---
    arena.register(user1)
    assert arena.get_user_by_id("test1") == user1
    with pytest.raises(LookupError):
        arena.get_user_by_name("test1")

    # Verificar que dos usuaris amb el mateix nom si poden existir, pero no amb el mateix ID
    arena.register(user2)
    assert arena.get_user_by_name("UserBot") == [user1, user2]
    with pytest.raises(UserRegistrationError):
        arena.register(User("UserBot", "test1"))
    
    # --- Delete user ---
    arena.delete_user(user2)
    assert arena.get_reg_players() == [user1]
    with pytest.raises(LookupError): # Eliminar un usuari que no existeix
        arena.delete_user(user2)
    with pytest.raises(LookupError):
        arena.get_user_by_id("test2")

    # --- Login ---
    assert user1.connected == False
    assert arena.get_log_players() == []

    # Fem login del usuari 1 i comprobem que tot s'hagi actualitzat correctament
    arena.login(user1)
    assert user1.connected == True
    assert arena.get_log_players() == [user1]
    with pytest.raises(LookupError): # Fer log a un usuari que no existeix
        arena.login(user2)
    with pytest.raises(UserLogError): # Fer log a un usuari que ja està connectat
        arena.login(user1)
    
    # --- Logout ---
    assert arena.get_log_players() == [user1]
    arena.logout(user1)
    assert arena.get_log_players() == []
    with pytest.raises(LookupError): # Desconnectar un jugador que no està registrat
        arena.logout(user2)
    with pytest.raises(UserLogError): # Desconnectar un jugador que ja ho està
        arena.logout(user1)

def test_games():
    arena = Arena(reg_users={}, con_users={}, current_games={})
    user1 = User("User 1", "test1")
    user2 = User("User 2", "test2")
    arena.register(user1)
    arena.register(user2)
    arena.login(user1)
    with pytest.raises(GameError): # No poden jugar si els dos no estan connectats
        game1 = arena.start_new_game(user1, user2)
    with pytest.raises(GameError): # No pot jugar un usuari contra si mateix
        game1 = arena.start_new_game(user1, user1)

    arena.login(user2)
    game1 = arena.start_new_game(user1, user2)
    assert arena.get_current_games() == [game1]
    with pytest.raises(GameError): # No poden jugar si ja estan en una partida en curs
        game2 = arena.start_new_game(user1, user2)
    arena.end_game(game1.id, False)
    assert arena.get_current_games() == []

    # Fem dues partides més
    game2 = arena.start_new_game(user1, user2)
    arena.end_game(game2.id, False)
    game3 = arena.start_new_game(user1, user2)
    with pytest.raises(GameError): # No es pot desconnectar si hi ha una partida en curs
        arena.logout(user2)
    with pytest.raises(GameError): # No es pot eliminar l'usuari si hi ha una partida en curs
        arena.delete_user(user2)
    found_game, seed = arena.get_game("test1", game2.id)
    assert found_game == game2
    assert seed == game2.seed

    # Comprobar que el user.in_game() funciona
    assert user2.in_game()
    arena.end_game(game3.id, True)   
    assert not user1.in_game()
    with pytest.raises(LookupError):
        arena.end_game(game3.id, True)   

    # Obtenir ranking
    ranking = arena.get_ranking() 
    assert ranking[0] == user2 # 66.67% winrate
    assert ranking[1] == user1 # 33,33% winrate
    assert user2.winrate() == 66.67 and user1.winrate() == 33.33

    # Cerca de partides
    user3 = User("User 3", "test3")
    assert arena.get_user_games(user1) == [game1, game2, game3]
    with pytest.raises(LookupError): # Buscar a un jugador que no es troba registrat
        arena.get_user_games(user3)
    with pytest.raises(LookupError): # Buscar a un jugador que no es troba registrat
        arena.get_game(user3.id, game2.id)
    arena.register(user3)
    arena.login(user3)
    with pytest.raises(LookupError): # Buscar una partida que no ha jugat
        arena.get_game(user3.id, game2.id)
    

if __name__ == "__main__":
    test_apply_move()