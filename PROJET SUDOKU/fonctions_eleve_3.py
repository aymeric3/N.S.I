# fonctions_eleve_3.py

def est_valide(grille, i, j, val):
    """
    Vérifie si une valeur peut être placée dans la case (i, j) sans violer les règles du Sudoku.
    """
    # Vérifier la ligne
    if val in ligne(grille, i):
        return False

    # Vérifier la colonne
    if val in colonne(grille, j):
        return False

    # Vérifier le bloc
    if val in bloc(grille, i, j):
        return False

    return True


def remplir_case(grille, i, j, val):
    """
    Remplit la case (i, j) avec la valeur val.
    """
    grille[i][j] = val


def vider_case(grille, i, j):
    """
    Vide la case (i, j).
    """
    grille[i][j] = 0


def grille_complete(grille):
    """
    Vérifie si la grille est complète (toutes les cases sont remplies).
    """
    for ligne in grille:
        if 0 in ligne:
            return False
    return True

# Fin du fichier fonctions_eleve_3.py