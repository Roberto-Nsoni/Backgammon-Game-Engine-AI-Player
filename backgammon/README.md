# Primera Pràctica d'AP2: Backgammon
En aquest projecte es desenvolupa un nucli d'un servidor de Backgammon.
    
S'implementa la lògica del joc, permet a dos persones jugar entre si, es programa un bot que pot jugar contra altres humans o bots... També s'implementa una `Arena` que compleix el rol de gestor de partides, el qual permet emmagatzemar dades d'usuaris, deixar que juguin entre ells...

## Esctructura del projecte
El projecte s'estructura en diferents mòduls on cadascun compleix un objectiu específic:

### 1. Mòdul `board.py`
Aquest mòdul és el cor del projecte. Aquí s'implementa tota la lògica i regles del joc, permet realitzar movimients legals i detectar moviments il·legals. Conté diferents classes:

- Classe `Dice`: 

    Serveix per representar el valor de dos daus.

- Classe `DiceCup`:

    Representa el gobelet on es barrejen els daus. Utilitza un generador congruencial per obtenir valors **pseudoaleatoris** així es pot simular el llançament dels daus.

- Classe `Jump`:

    Serveix per representar el salt d'**una** fitxa.

- Classe `Move`:

    Serveix per representar la tirada d'un jugador durant el seu torn i és una seqüència de salts d'algunes de les seves fitxes.

- Classe `Board`:

    Representa l'estat complert del tauler. 

### 2. Mòdul `human_vs_human.py`
Aquest mòdul permet la interacció per linea de comandes amb un tauler per fer una joc.
Inclou una funció per llegir i validar moviments per després actualitzar-los en un tauler.

Per més informació sobre com utilitzar `human_vs_human.py` vegeu l'apartat `"Com jugar?"`.

Addicionalment hi han dos moduls: `human_vs_bot.py` i `bot_vs_bot.py` amb els quals un humà pot jugar contra un bot i
també es pot visualitzar una partida "bot contra bot".

### 3. Mòdul `bot.py`

Aquest mòdul implementa una "intel·ligència artificial" que serveix per poder jugar contra un humà o contra un altre bot.

De manera general, l'elecció dels moviments és el resultat de:
1. Aplicar a tots els moviments possibles a de l'estat actual del tauler una funció de puntuació. 
2. Per a cada moviment, es simula la millor resposta del rival i es resta a la puntuació resultat. 
3. La jugada que tingui la puntuació més alta serà la jugada que es farà.

Les coses que es tenen en compte per aquesta funció d'evaluació son:

- La posició de cada fitxa al tauler
- L'objectiu principal del bot és fer "bear off"
- Penalitza tenir fitxes a la barra
- Pentalitza tenir fitxes soles

### 4. Mòdul `arena.py`:

Aquest mòdul compleix el rol de gestor d'usuaris i partides. Conté les següents classes:

- Classe `User`: Representació d'un usuari a la aplicació.
- Classe `Game`: Representa i gestiona una partida entre dos usuaris.
- Classe `Arena`: Gestiona l'arena on es juguen les partides, els usuaris registrats, connectats i les partides que estiguin actives en aquell moment.

## Característiques

1. **Persistència de Dades**: S'implementa un senzill que permet desar i recuperar un objecte Arena a/des d'un fitxer usant el mòdul `pickle`.

2. **Configuracions personalitzades**: Tant la classe `Board` com la classe `Arena` permet inicialitzar una configuració personalitzad (els valors predeterminats son els de una nova partida).

3. **Menú interactiu**: S'implementa un menú interactiu que permet als usuaris registrar-se, iniciar sessió, jugar partides, consular informació... per línia de comandes. Per poder jugar utilitzar-lo vegeu l'apartat `"Com jugar?"`.

4. **Proves unitaries**: Per garantir que la lògica del joc i la gestió interna de les partides de l'`arena` funcionen correctament, el projecte disposa de jocs de prova que faciliten detectar errors si en algun moment es decideix canviar alguna part.

## Com jugar?
Abans d'executar qualsevol programa, és important que es tingui instalat una versió igual o superior a Python 3.8.

El mode de joc recomenat es el mode arena, ja que des d'allà es pot accedir a la resta de mòduls sense posar una comanda per cada joc que es vulgui fer.

No obstant això, es pot accedir a un mòdul determinat i una partida concreta amb les comandes que s'expliquen a continuació:

### Jugar: Human Vs Human
Per jugar una partida entre dos humans, cal escriure a la lina de comandes el següent:

```bash
python human_vs_human.py
```

Per cada torn sortirá representat a la terminal l'estat actual del tauler (com a la següent de sota). Les fitxes vermelles representen el torn del jugador BLANC i les verdes la del NEGRE:

![terminal](images/show.png 'terminal')

Per poder intractuar amb el tauler escriviu la combinació de parells (posició, dau) que vulgueu i, si el moviment es vàlid, s'executarà. Per exemple, si escriviu `12 3 19 1` es mourà la fitxa en la posició `12` amb el dau `3` (és a dir mourà a la posició 12 + 3 = 15) i la fitxa en la posició `19` amb el dau `1`.

### IMPORTANT!!
1. En cas de que no es pugin fer moviments, simplement feu un "enter" a la terminal.

2. Si voleu saber la llista de moviments que teniu disponibles, escriviu `"?"`. De totes formes, si escriviu un moviment invàl·lid s'escriurà en la terminal la llista de moviments que podeu fer.

### Jugar: Human vs Bot
Per jugar una partida entre un humà i un bot, cal escriure a la lina de comandes el següent:

```python
python human_vs_bot.py
```
Funciona de manera similar al `"Human Vs Human` esmentat a l'apartat anterior. La única diferència es que l'humà jugarà sempre com a "blanc" i el bot jugarà automàticament com a "negre".

### Jugar: Bot Vs Bot
Per jugar una partida entre un humà i un bot, cal escriure a la lina de comandes el següent:

```python
python human_vs_bot.py
```

Funciona igual que el `Human Vs Bot`, però ara només juguen bots

### Jugar: Arena
Com s'a explicat abans, aquest és el mòdul recomenat per jugar:
Per executar-lo escriviu a la linea de comandes el següent:
```bash
python arena.py
```

Si **NO** és la primera vegada que executeu el programa un hauria de sortir un missatge conforme el mòdul `pickle` ha carregat correctament les dades emmagatzemades de les anteriors sessions.

Després, independentment de si és la primera vegada que l'executeu o no s'escriurà a la terminal un menú que permetrà navegar a traves de totes les funcionalitats de la arena.

Abans de tot, heu de registrar el vostre usuari. Aqui heu de indicar el vostre nom d'usuari *(ID)* que voleu mostrar a la resta de persones i el vostre nom real. Cal remarcar que **no poden existir dos usuaris amb el mateix *ID***. Si ja us heu registrat, heu d'iniciar sessió.

Un cop heu iniciat sessió podreu fer una de les següents coses:

0. Tancar la vostra sessió
1. Eliminar el vostre usuari
2. Jugar una partida (contra un altre humà o contra el bot de l'arena "JPetit")
3. Veure la llista d'usuaris registrats
4. Veure la llista d'usuaris connectats
5. Veure la llista de les partides en curs
6. Veure la llista de les partides d'un jugador
7. Veure el ranking de jugadors ordenats pel percentatge de victòries.

Per la lògica actual de la arena, només es pot jugar contra un bot, ja que no es pot tenir dues sessions iniciades a la mateixa terminal (:c)

## Execusió de Tests
Per provar que tot funciona correctament, el projecte compta amb unes proves unitàries que cobreixen alguns dels casos més comuns a l'hora de jugar, així com també alguns casos específics que puguin semblar conflictius per veure si es resolen de la manera esperada. Els tests cobreixen els mòduls que implementen la lògica del tauler del backgammon i de l'arena, les coses que estàn relacionades amb l'interficie no es proven. Podeu executar les proves amb la comanda:
```bash
python -m pytest .
```
