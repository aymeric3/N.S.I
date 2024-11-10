# affiche la grille de sudoku dans la console
def afficher_grille(grille):
    for ligne in grille:  # parcourt chaque ligne de la grille
        print(" ".join(str(x) if x != 0 else '.' for x in ligne))  # affiche chaque chiffre, remplaçant 0 par un point pour les cases vides

# remplit une case spécifique de la grille avec une valeur donnée
def remplir_case(grille, ligne, colonne, valeur):
    grille[ligne][colonne] = valeur  # place la valeur dans la case spécifiée

# vide une case spécifique de la grille
def vider_case(grille, ligne, colonne):
    grille[ligne][colonne] = 0  # met la case spécifiée à 0, indiquant une case vide

# vérifie si la grille est valide
def verifier_grille_valide(grille):
    for i in range(9):  # parcourt chaque ligne et colonne
        ligne = set()  # initialise un ensemble pour la ligne
        colonne = set()  # initialise un ensemble pour la colonne
        for j in range(9):  # parcourt chaque case de la ligne et de la colonne
            # vérifie la validité de la ligne
            if grille[i][j] != 0:
                if grille[i][j] in ligne:  # si le nombre est déjà présent dans la ligne
                    return False  # retourne False si la ligne est invalide
                ligne.add(grille[i][j])  # ajoute le nombre à l'ensemble ligne
            # vérifie la validité de la colonne
            if grille[j][i] != 0:
                if grille[j][i] in colonne:  # si le nombre est déjà présent dans la colonne
                    return False  # retourne False si la colonne est invalide
                colonne.add(grille[j][i])  # ajoute le nombre à l'ensemble colonne
    return True  # retourne True si la grille est valide
