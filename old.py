import random
from tkinter import *

def grille_vierge(n, p):
    """
    Renvoie un tableau de taille n*p
    qui représente le labyrinthe.
    Chaque case contient une liste de 4
    booléens qui indique si la voie vers
    [haut, bas, gauche, droite] est ouverte
    """
    L = []
    for i in range(n):
        P = []
        for j in range(p):
            P.append([i != 0, i != n - 1, j != 0, j != p - 1])
        L.append(P)

    return L


def deplacement(grille, i, j, direction):
    """
    Renvoie la case où arrive un
    joueur placé en (i,j) si il se
    déplace dans la direction direction
    dans grille
    """
    a = i
    b = j
    try:
        if direction == 0:
            while grille[a][b][direction]:
                a -= 1
        elif direction == 1:
            while grille[a][b][direction]:
                a += 1
        elif direction == 2:
            while grille[a][b][direction]:
                b -= 1
        elif direction == 3:
            while grille[a][b][direction]:
                b += 1
    except:
        pass
    return (a, b)


def distance_fin(grille, ifin, jfin, direction, k=None):
    """
    Renvoie un tableau T tel que T[a][b]
    est le nombre de déplacements
    nécessaires pour rejoindre l'arrivée
    situé en ifin,jfin en partant de a,b
    """
    n = len(grille)
    p = len(grille[0])
    if k == None:
        k = n * p
    T = []
    for a in range(n):
        P = []
        for b in range(p):
            P.append(2E308)
        T.append(P)
    if k == 1:
        for a in range(n):
            for b in range(p):
                if deplacement(grille, a, b, direction) == (ifin, jfin):
                    T[a][b] = 1
        return T
    else:
        U = distance_fin(grille, ifin, jfin, direction, k - 1)
        for a in range(n):
            for b in range(p):
                T[a][b] = U[a][b]
                for d in range(4):
                    (c, d) = deplacement(grille, a, b, d)
                    if U[c][d] + 1 < T[a][b]:
                        T[a][b] = 1 + U[c][d]
        return T


def ajoute_barriere(grille, i, j, direction):
    """
    Renvoie la nouvelle valeur de grille
    où on a ajouté une barrière à côté de
    la case (i,j) dans la direction direction
    """
    n = len(grille)
    p = len(grille[0])
    grille_2 = []
    for a in range(n):
        P = []
        for b in range(p):
            C = []
            for d in range(4):
                C.append(grille[a][b][d])
            P.append(C)
        grille_2.append(P)
    grille_2[i][j][direction] = False
    if direction == 0 and i != 0:
        grille_2[i - 1][j][1] = False
    elif direction == 1 and i != n - 1:
        grille_2[i + 1][j][0] = False
    elif direction == 2 and j != 0:
        grille_2[i][j - 1][3] = False
    elif direction == 3 and j != p - 1:
        grille_2[i][j + 1][2] = False
    return grille_2


def retire_barriere(grille, i, j, direction):
    """
    Renvoie la nouvelle valeur de grille
    où on a retiré une barrière à côté de
    la case (i,j) dans la direction direction
    """
    n = len(grille)
    p = len(grille[0])
    grille_2 = []
    for a in range(n):
        P = []
        for b in range(p):
            C = []
            for d in range(4):
                C.append(grille[a][b][d])
            P.append(C)
        grille_2.append(P)
    grille_2[i][j][direction] = True
    if direction == 0 and i != 0:
        grille_2[i - 1][j][1] = True
    elif direction == 1 and i != n - 1:
        grille_2[i + 1][j][0] = True
    elif direction == 2 and j != 0:
        grille_2[i][j - 1][3] = True
    elif direction == 3 and j != p - 1:
        grille_2[i][j + 1][2] = True
    return grille_2


def affiche_grille(grille, ifin, jfin, direction):
    n = len(grille)
    p = len(grille[0])
    fenetre = Tk()
    canvas = Canvas(fenetre, width=38 * (p + 2), height=38 * (n + 2), background='white')
    for i in range(n):
        for j in range(p):
            if not (grille[i][j][0]) and (i, j, 0) != (ifin, jfin, direction):
                canvas.create_line(38 * (j + 1), 38 * (i + 1), 38 * (j + 2), 38 * (i + 1))
            if not (grille[i][j][1]) and (i, j, 1) != (ifin, jfin, direction):
                canvas.create_line(38 * (j + 1), 38 * (i + 2), 38 * (j + 2), 38 * (i + 2))
            if not (grille[i][j][2]) and (i, j, 2) != (ifin, jfin, direction):
                canvas.create_line(38 * (j + 1), 38 * (i + 1), 38 * (j + 1), 38 * (i + 2))
            if not (grille[i][j][3]) and (i, j, 3) != (ifin, jfin, direction):
                canvas.create_line(38 * (j + 2), 38 * (i + 1), 38 * (j + 2), 38 * (i + 2))
    """
    photo = PhotoImage(file="point_rouge.jpg")
    (i,j) = (idebut,jdebut)
    canvas.create_image(38 * (j+1), 38 * (i+1)+4, anchor=NW, image=photo)
    Button(fenetre, text ='Droite').pack(side=RIGHT, padx=5, pady=5)
    Button(fenetre, text ='Gauche').pack(side=RIGHT, padx=5, pady=5)
    Button(fenetre, text ='Bas').pack(side=RIGHT, padx=5, pady=5)
    Button(fenetre, text ='Haut').pack(side=RIGHT, padx=5, pady=5)
    """
    canvas.pack()
    fenetre.mainloop()


def chemin(grille, idebut, jdebut, ifin, jfin, direction):
    """
    Renvoie le chemin le plus court pour atteindre
    l'arrivée en partant de (idebut,jdebut)
    """
    T = distance_fin(grille, ifin, jfin, direction)
    (i, j) = (idebut, jdebut)
    L = [(i, j)]
    while T[i][j] != 1:
        d = 0
        while d < 4:
            (a, b) = deplacement(grille, i, j, d)
            if T[a][b] < T[i][j]:
                (i, j) = (a, b)
                d = 4
            d += 1
        L.append((i, j))
    return L


def difficulte(grille, ifin, jfin, direction, k=None):
    """
    Renvoie un tableau T tel que T[a][b]
    est le nombre d'occasions de se tromper
    sur un chemin pour rejoindre l'arrivée
    situé en ifin,jfin en partant de a,b
    """
    n = len(grille)
    p = len(grille[0])
    if k == None:
        k = n * p
    T = []
    for a in range(n):
        P = []
        for b in range(p):
            P.append(2E308)
        T.append(P)
    if k == 1:
        for a in range(n):
            for b in range(p):
                if deplacement(grille, a, b, direction) == (ifin, jfin):
                    T[a][b] = 1
        return T
    else:
        U = difficulte(grille, ifin, jfin, direction, k - 1)
        for a in range(n):
            for b in range(p):
                T[a][b] = U[a][b]
                possibilite = 0
                for d in range(4):
                    (c, d) = deplacement(grille, a, b, d)
                    if (c, d) != (a, b):
                        possibilite += 1
                for d in range(4):
                    (c, d) = deplacement(grille, a, b, d)
                    if U[c][d] + 1 < T[a][b]:
                        T[a][b] = U[c][d] + possibilite - 1
        return T


def note_grille(grille, ifin, jfin, direction):
    n = len(grille)
    p = len(grille[0])
    dif = distance_fin(grille, ifin, jfin, direction)
    (idebut, jdebut) = (ifin, jfin)
    for i in range(n):
        for j in range(p):
            if dif[i][j] > dif[idebut][jdebut] and dif[i][j] < 1E100:
                (idebut, jdebut) = (i, j)
    return [(idebut, jdebut), dif[idebut][jdebut]]


def genere_grille(n, p, ifin, jfin, direction):
    grille = grille_vierge(n, p)
    (idebut, jdebut) = (ifin, jfin)
    for compt in range(n * p):
        i = random.randint(0, n - 1)
        j = random.randint(0, p - 1)
        d = random.randint(0, 3)
        grille2 = ajoute_barriere(grille, i, j, d)
        note = note_grille(grille2, ifin, jfin, direction)
        note_originale = note_grille(grille, ifin, jfin, direction)
        # print(note)
        if note_originale[1] <= note[1]:
            grille = grille2
            (idebut, jdebut) = note[0]
    return [grille, (idebut, jdebut)]


"""
grille = grille_vierge(3,2)
print(grille)
#ajoute_barriere(grille,0,0,1)
#print(distance_fin(grille,2,0,1))
#print(chemin(grille,0,0,2,0,1))
#print(difficulte(grille,2,0,1))
print(note_grille(grille,2,0,1))
affiche_grille(grille,2,0,1)
"""

G = genere_grille(15, 15, 14, 5, 1)
grille = G[0]
(idebut, jdebut) = G[1]
print((idebut, jdebut))
print(note_grille(grille, 14, 5, 1))
print(chemin(grille, idebut, jdebut, 14, 5, 1))
affiche_grille(grille, 14, 5, 1)
