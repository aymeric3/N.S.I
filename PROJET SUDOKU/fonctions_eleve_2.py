# fonctions_eleve_2.py

def possibles(grille, i, j):
    """
    Retourne les chiffres possibles pour la case (i, j) en fonction des règles du Sudoku.
    """
    if grille[i][j] != 0:
        return []  # La case est déjà remplie

    chiffres_ligne = ligne(grille, i)
    chiffres_colonne = colonne(grille, j)
    chiffres_bloc = bloc(grille, i, j)

    return [val for val in range(1, 10) if val not in chiffres_ligne and val not in chiffres_colonne and val not in chiffres_bloc]

def suivante(i, j):
    """
    Retourne les coordonnées de la case suivante à (i, j).
    """
    if j < 8:
        return i, j + 1
    elif i < 8:
        return i + 1, 0
    else:
        return 9, 0  # Fin de la grille

# Fin du fichier fonctions_eleve_2.py