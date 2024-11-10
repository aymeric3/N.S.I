# retourne les chiffres présents dans une ligne spécifique
def ligne(grille, index):
    return [x for x in grille[index] if x != 0]  # renvoie les chiffres non nuls de la ligne

# retourne les chiffres présents dans une colonne spécifique
def colonne(grille, index):
    return [grille[i][index] for i in range(9) if grille[i][index] != 0]  # renvoie les chiffres non nuls de la colonne

# retourne les chiffres présents dans le bloc 3x3 auquel appartient une case donnée
def bloc(grille, ligne, colonne):
    ligne_debut = (ligne // 3) * 3  # calcule la première ligne du bloc
    colonne_debut = (colonne // 3) * 3  # calcule la première colonne du bloc
    return [
        grille[r][c]
        for r in range(ligne_debut, ligne_debut + 3)
        for c in range(colonne_debut, colonne_debut + 3)
        if grille[r][c] != 0  # filtre les chiffres non nuls du bloc
    ]

# retourne la liste des chiffres possibles pour une case donnée
def possibles(grille, ligne, colonne):
    if grille[ligne][colonne] != 0:  # si la case est déjà remplie
        return []  # retourne une liste vide
    chiffres = set(range(1, 10))  # initialise l'ensemble des chiffres possibles
    chiffres -= set(ligne(grille, ligne))  # retire les chiffres de la ligne
    chiffres -= set(colonne(grille, colonne))  # retire les chiffres de la colonne
    chiffres -= set(bloc(grille, ligne, colonne))  # retire les chiffres du bloc
    return list(chiffres)  # retourne la liste des chiffres restants
