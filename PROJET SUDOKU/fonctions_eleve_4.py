# fonctions_eleve_4.py

from fonctions_eleve_1 import ligne, colonne, bloc
from fonctions_eleve_2 import suivante

def resoudre(grille, i=0, j=0):
    """
    Résout la grille de Sudoku en utilisant une approche récursive.
    """
    if i == 9:
        return True  # La grille est résolue

    if grille[i][j] != 0:
        next_i, next_j = suivante(i, j)
        return resoudre(grille, next_i, next_j)
    else:
        for val in range(1, 10):
            if val not in ligne(grille, i) and val not in colonne(grille, j) and val not in bloc(grille, i, j):
                grille[i][j] = val
                next_i, next_j = suivante(i, j)
                if resoudre(grille, next_i, next_j):
                    return True
                grille[i][j] = 0  # Backtracking

    return False

# Fin du fichier fonctions_eleve_4.py
