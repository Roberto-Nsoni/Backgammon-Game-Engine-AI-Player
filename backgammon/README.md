# AP2 - Backgammon
- Carta de presentació, com a projecte.
- 

!!! IMPORTANT Si surt '[ERRNº 2] No such file or directory' es perquè la funció draw no troba les imatges que haurien d'estar a .\images
Si executeu el programa desde VSC i no executeu exactament '.\human_vs_human.py' (per exemple, si esteu a ".\backgammon\human_vs_human.py)
no el trobarà.
Per solucionar-ho:
    1 - A dalt a la esquerra: File -> open folder -> assegureu-vos d'obrir la carpeta 'backgammon' amb el human_vs_human.py inmediatament dins
    2 - Executeu el programa desde la terminal
    3 - Canvieu les lines 77, 83, 91: draw(board, f.png) --> show(f.png)
