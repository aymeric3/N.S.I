# fonctions_eleve_1.py (AYMERIC)

def ligne(grille, i):
    """
    renvooie les chiffres présents sur la ligne i de la grille.
    """
    return [val for val in grille[i] if val != 0]

def colonne(grille, j):
    """
    renvoie les chiffres présents sur la colonne j de la grille.
    """
    return [grille[i][j] for i in range(9) if grille[i][j] != 0]

def bloc(grille, i, j):
    """
    retourne les chiffres présents dans le bloc 3x3 correspondant à la case (i, j).
    """
    bloc_ligne = (i // 3) * 3
    bloc_colonne = (j // 3) * 3
    return [grille[x][y] for x in range(bloc_ligne, bloc_ligne + 3) for y in range(bloc_colonne, bloc_colonne + 3) if grille[x][y] != 0]