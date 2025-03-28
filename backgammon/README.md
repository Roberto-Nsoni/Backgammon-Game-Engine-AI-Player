# 🎲 Primera Pràctica d'AP2: Backgammon
Benvinguts a la primera pràctica de l'assignatura d'AP2!

En aquest projecte es desenvolupa un nucli d'un servidor del joc de taula per a dues persones  anomenat "Backgammon".
    
S'implementa la lògica del joc, permet a dues persones jugar entre si, es programa un bot que pot jugar contra altres humans o bots... També s'implementa una `Arena` que compleix el rol de gestor de partides, el qual permet emmagatzemar dades d'usuaris, deixar que juguin entre ells...

## 🗂️ Estructura del projecte
El projecte s'estructura en diferents mòduls on cadascun compleix un objectiu específic:

### 1. Mòdul `board.py`
Aquest mòdul és el cor del projecte. Aquí s'implementa tota la lògica i regles del joc, permet realitzar moviments legals i detectar moviments il·legals. Conté diferents classes:

- Dataclass `Dice`: 

    Serveix per representar el valor de dos daus.

- Class `DiceCup`:

    Representa el gobelet on es barregen els daus. Utilitza un generador congruencial per obtenir valors **pseudoaleatoris** així es pot simular el llançament dels daus.

- Dataclass `Jump`:

    Serveix per representar el salt d'**una** fitxa.

- Dataclass `Move`:

    Serveix per representar la tirada d'un jugador durant el seu torn i és una seqüència de salts d'algunes de les seves fitxes.

- Classe `Board`:

    Representa l'estat complet del tauler. 

### 2. Mòdul `human_vs_human.py`
Aquest mòdul permet la interacció per línia de comandes amb un tauler per fer un joc.
Inclou una funció per llegir i validar moviments per després actualitzar-los en un tauler.

Per a més informació sobre com utilitzar `human_vs_human.py` vegeu l'apartat `"Com jugar?"`.

Addicionalment, hi ha dos mòduls: `human_vs_bot.py` i `bot_vs_bot.py` amb els quals un humà pot jugar contra un bot i també es pot visualitzar una partida "bot contra bot".

### 3. Mòdul `bot.py`

Aquest mòdul implementa una "intel·ligència artificial" que serveix per poder jugar contra un humà o contra un altre bot.

De manera general, l'elecció dels moviments és el resultat de:
1. Assignar a cada moviment possible de l'estat actual del tauler una puntuació mitjançant una funció d'avaluació. 
2. Per a cada moviment, se simula la millor resposta del rival i es resta a la puntuació resultant. 
3. La jugada que tingui la puntuació més alta serà la jugada que es farà.

Les coses que es tenen en compte per aquesta funció d'avaluació són:

- La posició de cada fitxa al tauler
- L'objectiu principal del bot és fer "bear off"
- Penalitza tenir fitxes a la barra
- Penalitza tenir fitxes soles

### 4. Mòdul `arena.py`:

Aquest mòdul compleix el rol de gestor d'usuaris i partides. Conté les següents classes:

- Dataclass `User`:

    Representació d'un usuari a l'aplicació. Emmagatzema q informació com el nom d'usuari, el numero de partides jugades i guanyades, la llista de partides, l'estatus connectat/desconnectat...

- Dataclass `Game`:
    
    Representa i gestiona una partida entre dos usuaris. Conté informació com els usuaris que juguen, la llavor del gobelet, l'estat del tauler, el nombre de moviments, l'estatus en curs/acabat...

- Classe `Arena`:

    Gestiona l'arena on es juguen les partides, els usuaris registrats, connectats i les partides que estiguin actives en aquell moment.

A més, es defineixen unes excepcions específiques que ajuden a gestionar de millor manera els diferents errors que es poden produir durant la interacció amb l'aplicació:

- `UserRegistrationError`: Aquesta excepció s'eleva quan es produeix un error relacionat amb el registre d'usuaris, per exemple, si s'intenta registrar un usuari amb un ID que ja hi està registrat.

- `UserLogError`: S'utilitza per a errors relacionats amb el login/logout dels usuaris. Per exemple, es pot generar quan s'intenta tancar la sessió d'un usuari que ja està desconnectat.

- `GameError`: S'aixeca per errors relacionats amb la gestió interna de les partides, per exemple, quan s'intenta eliminar un usuari que encara participa en una partida.

## ✨ Característiques

1. **Persistència de Dades**: S'implementa un senzill que permet desar i recuperar un objecte Arena a/des d'un fitxer usant el mòdul `pickle`.

2. **Configuracions personalitzades**: Tant la classe `Board` com la classe `Arena` permet inicialitzar una configuració personalitzada (els valors predeterminats són els d'una nova partida).

3. **Menú interactiu**: S'implementa un menú interactiu que permet als usuaris registrar-se, iniciar sessió, jugar partides, consular informació... per línia de comandes. Per poder jugar utilitzar-lo vegeu l'apartat `"Com jugar?"`.

4. **Proves unitàries**: Per garantir que la lògica del joc i la gestió interna de les partides de l'`arena` funcionen correctament, el projecte disposa de jocs de prova que faciliten detectar errors si en algun moment es decideix canviar alguna part.

## 🎮 Com jugar?
Abans d'executar qualsevol programa, és important que es tingui instal·lat una versió igual o superior a Python 3.8, ja que totes les dependències i llibreries que s'utilitzen en aquest projecte es troben a la biblioteca estàndard. Les llibreries utilitzades son: future, cataclasses, typing, sys, random, uuid, pickle i pytest.

També és pots trobar el detall de les regles del backgammon a https://www.bkgm.com/rules.html i és convenient que es tinguin ben clares.

El mode de joc recomanat és el mode arena, perquè des d'allà es pot accedir a la resta de mòduls sense posar una comanda per cada joc que es vulgui fer. No obstant això, es pot accedir a un mòdul determinat i una partida concreta amb les comandes que s'expliquen a continuació:

### Jugar: Human Vs. Human
Per jugar una partida entre dos humans, cal escriure a la línia de comandes el següent:

```bash
python human_vs_human.py
```

Per a cada torn sortirà, representat a la terminal, l'estat actual del tauler (com a la imatge de sota). Les fitxes vermelles representen el torn del jugador BLANC i les verdes la del NEGRE:

![terminal](images/show.png 'terminal')

Per poder interactuar amb el tauler escriviu la combinació de parells (posició, dau) que vulgueu i, si el moviment és vàlid, s'executarà. Per exemple, si escriviu `12 3 19 1` es mourà la fitxa en la posició `12` amb el dau `3` (és a dir mourà a la posició 12 + 3 = 15) i la fitxa en la posició `19` amb el dau `1`.

#### ❗❗NOTA 1: Comandes especials❗❗
- **Consultar moviments disponibles**: Si voleu saber la llista de moviments que teniu disponibles, escriviu `"?"`. De totes maneres, si doneu un moviment invàlid, s'escriurà en la terminal la llista de moviments que podeu fer.

- **Representació de la barra**: La posició de la barra es representa amb el número `0`.

- **Pasar el torn**: En cas que no es puguin fer moviments, simplement s'ha de prémer "enter" a la terminal (sense introduir cap comanda).

Les llavors que s'utilitzen per generar els daus pseudoaleatoris en `human_vs_human.py`, `human_vs_bot.py`, `bot_vs_bot.py` són les mateixes en totes les partides, per canviar la generació dels daus, s'ha de canviar manualment el valor de la variable `seed`.

### Jugar: Human Vs. Bot
Per jugar una partida entre un humà i un bot, cal escriure a la lina de comandes el següent:

```python
python human_vs_bot.py
```
Funciona de manera similar al `"Human Vs. Human` esmentat a l'apartat anterior. L'única diferència es que l'humà jugarà sempre com a "blanc" i el bot jugarà automàticament com a "negre".

### Jugar: Bot Vs. Bot
Per jugar una partida entre un humà i un bot, cal escriure a la línia de comandes el següent:

```python
python human_vs_bot.py
```

Funciona igual que el `Human Vs. Bot`, però ara només juguen bots

### Jugar: Arena
Com s'ha explicat abans, aquest és el mòdul recomanat per jugar:
Per executar-lo escriviu a la línia de comandes el següent:
```bash
python arena.py
```

Si **NO** és la primera vegada que executeu el programa us hauria de sortir un missatge confirmant que el mòdul `pickle` ha carregat correctament les dades emmagatzemades de les anteriors sessions.

Després, independentment de si és la primera vegada que l'executeu o no s'escriurà a la terminal un menú que permetrà navegar a través d'algunes de les funcionalitats de l'`Arena`.

Abans de tot, heu de registrar el vostre usuari. Aquí heu d'indicar el vostre nom d'usuari *(ID)* que voleu mostrar a la resta de persones i el vostre nom real. Cal remarcar que **no poden existir dos usuaris amb el mateix *ID***. Si ja us heu registrat, heu d'iniciar sessió.

Un cop heu iniciat sessió podreu accedir a les funcionalitats completes de l'`Arena`. Es poden fer una de les següents coses:

0. Tancar la vostra sessió
1. Eliminar el vostre usuari
2. Jugar una partida (contra un altre humà o contra el bot de l'arena "JPetit")
3. Veure la llista d'usuaris registrats
4. Veure la llista de les partides en curs
5. Veure en detall el perfil d'un usuari
6. Veure en detall la partida d'un usuari
7. Veure el ranking de jugadors ordenats pel percentatge de victòries.

#### ⚠️ NOTA 2: Consideracions importants ⚠️
**Encara que algunes coses no es puguin fer directament desde la terminal, si estan internament implementades:**

- Per tal d'evitar una experiència aclaparadora, només estan disponibles les funcionalitats més rellevants que l'`Arena` ofereix (per exemple, l'opció de veure en detall el perfil d'un usuari només està acotat només pel seu nom d'usuari). 

- Per la lògica actual del menú de l'`Arena`, només es pot jugar contra un bot, ja que no es pot tenir dues sessions iniciades a la mateixa terminal (:c)

## ✅ Execució de Tests
Per provar que tot funciona correctament, el projecte compta amb unes proves unitàries que cobreixen alguns dels casos més comuns a l'hora de jugar, així com alguns casos específics que puguin semblar conflictius per veure si es resolen de la manera esperada. Els tests cobreixen els mòduls que implementen la lògica del tauler del backgammon i de l'arena, les coses que estan relacionades amb l'interfície no es proven. Podeu executar les proves amb la comanda:
```bash
python -m pytest .
```
