import numpy as np
from collections import deque
from itertools import product
import sys


def grille_vierge(n, p):
    """
    Renvoie un tableau de taille n*p
    qui représente le labyrinthe.
    Chaque case contient une liste de 4
    booléens qui indique si la voie vers
    [haut, bas, gauche, droite] est ouverte
    """
    grille = np.zeros((n, p, 4), dtype=bool)

    grille[:, :] = (True, True, True, True)

    grille[0, 1:-1] = (False, True, True, True)  # haut
    grille[-1, 1:-1] = (True, False, True, True)  # bas
    grille[1:-1, 0] = (True, True, False, True)  # gauche
    grille[1:-1, -1] = (True, True, True, False)  # droite

    grille[0, 0] = (False, True, False, True)
    grille[0, -1] = (False, True, True, False)
    grille[-1, 0] = (True, False, False, True)
    grille[-1, -1] = (True, False, True, False)

    return grille


def deplacement(grille, p, direction):
    """
    Renvoie la case où arrive un
    joueur placé en (i,j) si il se
    déplace dans la direction direction
    dans grille
    """
    a, b = p
    while 0 <= a < grille.shape[0] and 0 <= b < grille.shape[1] and grille[a][b][direction]:
        if direction == 0:
            a -= 1
        elif direction == 1:
            a += 1
        elif direction == 2:
            b -= 1
        elif direction == 3:
            b += 1
    return a, b


def distance_fin(grille, fin, direction):
    """
    Renvoie un tableau T tel que T[a][b]
    est le nombre de déplacements
    nécessaires pour rejoindre l'arrivée
    situé en ifin,jfin en partant de a,b
    """

    def f(a, b, d):
        if d == 0:
            a -= 1
        elif d == 1:
            a += 1
        elif d == 2:
            b -= 1
        elif d == 3:
            b += 1
        return a, b

    n, p = grille.shape[:2]

    T = np.ones((n, p)) * np.inf

    old_deque = deque()

    a, b = fin
    T[a, b] = 1
    old_deque.append((a, b))
    d = [1, 0, 3, 2][direction]
    while grille[a, b][d]:
        a, b = f(a, b, d)
        T[a, b] = 1
        old_deque.append((a, b))

    for i in range(1, n * p):
        new_deque = deque()
        for t in old_deque:
            for d in range(4):
                d_i = [1, 0, 3, 2][d]
                if not grille[t][d_i] and grille[t][d]:
                    a, b = f(t[0], t[1], d)
                    while grille[a, b][d]:
                        if T[a, b] == np.inf:
                            T[a, b] = i + 1
                            new_deque.append((a, b))
                        a, b = f(a, b, d)
                    if T[a, b] == np.inf:
                        T[a, b] = i + 1
                        new_deque.append((a, b))
        old_deque = new_deque
    return T


def est_connexe(grille, T, debut):
    l = np.argwhere(T == np.inf)
    return len([k for k in l if relies(grille, debut, tuple(k))]) == 0


def note_grille(grille, fin, direction):
    """
    Donne la note d'une grille ainsi que le point de départ
    :param grille: grille
    :param i_fin: i_fin
    :param j_fin: j_fin
    :param direction: direction finale
    :return: [(i_debut, j_debut), note, T]
    """
    n, p = grille.shape[:2]
    T = distance_fin(grille, fin, direction)
    T_tmp = T.copy()
    T_tmp[T_tmp == np.inf] = -np.inf
    debut = np.unravel_index(np.argmax(T_tmp), T_tmp.shape)
    if est_connexe(grille, T, debut) or True:
        # U = nombre_chemins(grille)
        # delta, distance = deltas_and_distance(grille, T, debut, fin)
        # note = delta + distance + T_tmp.max() * 100 + nombre_choix(grille, T, debut, fin, 10)
        # note = nombre_choix(grille, T, debut, fin, 2)
        note = 10 * T_tmp.max() - angles(grille)
        # print(angles(grille))
        return debut, note, T
    else:
        return None, 0, None


def modifier_barriere(grille, i, j, direction, valeur, copy=False):
    """
    Renvoie la nouvelle valeur de grille
    où on a ajouté une barrière à côté de
    la case (i,j) dans la direction direction
    """
    grille_copy = grille.copy() if copy else grille
    grille_copy[i, j][direction] = valeur

    if direction == 0 and i != 0:  # haut
        grille_copy[i - 1, j][1] = valeur
    elif direction == 1 and i != grille.shape[0] - 1:  # bas
        grille_copy[i + 1, j][0] = valeur
    elif direction == 2 and j != 0:  # gauche
        grille_copy[i, j - 1][3] = valeur
    elif direction == 3 and j != grille.shape[1] - 1:  # droite
        grille_copy[i, j + 1][2] = valeur

    return grille_copy

def angles(grille):
    c = 0
    for i in range(grille.shape[0]):
        for j in range(grille.shape[1]):
            haut, bas, gauche, droite = grille[i, j]
            if (not haut or not bas) and not gauche:
                c += 1
            if (not haut or not bas) and not droite:
                c += 1
    return c

def chemin(grille, T, debut, fin):
    """
    Renvoie le chemin le plus court pour atteindre
    l'arrivée en partant de (idebut,jdebut)
    """
    p = debut
    L = [p]
    while p != fin:
        l = [deplacement(grille, p, d) for d in range(4)]
        p = l[np.argmin([T[k] for k in l])]
        L.append(p)

    return L


def nombre_choix(grille, T, debut, fin, x):
    p = debut
    c = 0
    while p != fin:
        l = [deplacement(grille, p, d) for d in range(4)]
        p = l[np.argmin([T[k] for k in l])]
        c += 1
        k = sum(grille[p])
        if k > 2:
            c += k * x
    return c


def deltas_and_distance(grille, T, debut, fin):
    p = debut
    delta = 0
    distance = 0
    while p != fin:
        q = p
        l = [deplacement(grille, p, d) for d in range(4)]
        p = l[np.argmin([T[k] for k in l])]
        delta += sum([T[p] - T[q] for p in l])
        distance += abs(q[0] + q[1] - p[0] - p[1])
    return delta, distance


def nombre_chemins(grille):
    n, p = grille.shape[:2]
    U = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            for k in range(n):
                for l in range(p):
                    if (i, j) != (k, l):
                        U[i, j] += int(relies(grille, (k, l), (i, j)))
    return U


def relies(grille, debut, fin):
    pile = deque([debut])
    visite = np.zeros(grille.shape[:2], dtype=bool)

    while len(pile) != 0:
        u = pile.pop()
        if u == fin:
            return True
        for d in range(4):
            if grille[u][d]:
                v = deplacement(grille, u, d)
                if not visite[v]:
                    visite[v] = True
                    pile.append(v)
    return False


def genere_grille_aux(n, p, position_fin, direction):
    """
    Génère une grille de labyrinthe
    :param n: hauteur
    :param p: largeur
    :param position_fin: ordonné en partant du haut, abscisse en partant de la gauche
    :param direction: entier compris dans [0,3] représentant [haut, bas, gauche, droite]
    :return: [grille, position de début]
    """
    grille = grille_vierge(n, p)
    best_position, best_note, best_T = position_fin, 1, None
    for k in range(n * p):
        if k % max(1, int(n * p / 10)) == 0:
            print("Note: {}, {}%".format(best_note, round(100 * k / (n * p * 2), 1)))

        i = np.random.randint(n)
        j = np.random.randint(p)
        d = np.random.randint(4)

        if not ((d == 0 and i == 0) or (d == 1 and i == n - 1) or (d == 2 and j == 0) or (d == 3 and j == p - 1)):
            modifier_barriere(grille, i, j, d, False)

            position, note, T = note_grille(grille, position_fin, direction)

            if best_note <= note < n * p + 1:
                best_position = position
                best_note = note
                best_T = T
            else:
                modifier_barriere(grille, i, j, d, True)

    best_chemin = []  # chemin(grille, best_T, best_position, position_fin)
    grille[position_fin][direction] = True
    return grille, best_position, best_T, best_chemin, best_note


def genere_grille(n, p, position_fin, direction):
    best_grille, best_position, best_T, best_chemin, best_note = None, None, None, None, -50
    l = 5
    for k in range(l):
        if k % 1 == 0:
            print("Best Note: {}, {}%".format(best_note, round(100 * k / l, 1)))
        grille, position, T, chemin, note = genere_grille_aux(n, p, position_fin, direction)
        if note > best_note:
            best_grille, best_position, best_T, best_chemin, best_note = grille, position, T, chemin, note

    return best_grille, best_position, best_T, best_chemin


if __name__ == "__main__":
    genere_grille(25, 25, (0, 10), 0)
