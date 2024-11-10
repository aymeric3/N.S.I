# vérifie et applique la technique des singletons nus
def singleton_nu(grille):
    for r in range(9):  # parcourt chaque ligne
        for c in range(9):  # parcourt chaque colonne
            if grille[r][c] == 0:  # si la case est vide
                options = possibles(grille, r, c)  # obtient les options possibles pour la case
                if len(options) == 1:  # si une seule option est possible
                    grille[r][c] = options[0]  # remplit la case avec cette option

# vérifie et applique la technique des paires nues
def paires_nues(grille):
    # (implémentation ici selon la logique spécifique des paires nues)
    pass  # placeholder pour le code des paires nues

# vérifie et applique la technique des triplets nus
def triplets_nus(grille):
    # (implémentation ici selon la logique spécifique des triplets nus)
    pass  # placeholder pour le code des triplets nus

# vérifie et applique la technique des singletons cachés
def singletons_caches(grille):
    # (implémentation ici selon la logique spécifique des singletons cachés)
    pass  # placeholder pour le code des singletons cachés
