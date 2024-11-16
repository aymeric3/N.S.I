# sudoku.py
import tkinter as tk
from fonctions_eleve_1 import *
from fonctions_eleve_2 import *
from fonctions_eleve_3 import *
from fonctions_eleve_4 import *


def afficher_grille(grille, canvas, entrees):
    """
    Affiche la grille de Sudoku sur le canvas.
    """
    canvas.delete("all")
    for i in range(9):
        for j in range(9):
            x1, y1 = j * 60, i * 60
            x2, y2 = x1 + 60, y1 + 60
            canvas.create_rectangle(x1, y1, x2, y2, width=2)
            if grille[i][j] != 0:
                canvas.create_text(x1 + 30, y1 + 30, text=str(grille[i][j]), font=("Arial", 24))
            else:
                entrees[i][j] = tk.Entry(canvas, width=2, font=("Arial", 24), justify='center')
                entrees[i][j].place(x=x1 + 10, y=y1 + 10, width=40, height=40)
                entrees[i][j].bind("<FocusOut>", lambda e, i=i, j=j: verifier_et_valider(grille, canvas, entrees, i, j))
                entrees[i][j].bind("<KeyRelease>", lambda e: filtrer_entree(e))


def filtrer_entree(event):
    """
    Empêche la saisie de caractères non numériques ou de chiffres en dehors de 1-9.
    """
    widget = event.widget
    valeur = widget.get()
    if not valeur.isdigit() or not (1 <= int(valeur) <= 9):
        widget.delete(0, tk.END)


def verifier_entree(grille, i, j, val):
    """
    Vérifie si la valeur entrée est valide pour la case donnée.
    """
    return val not in ligne(grille, i) and val not in colonne(grille, j) and val not in bloc(grille, i, j)


def verifier_et_valider(grille, canvas, entrees, i, j):
    """
    Vérifie la saisie de l'utilisateur et valide ou efface l'entrée.
    """
    try:
        val = int(entrees[i][j].get())
        if 1 <= val <= 9 and verifier_entree(grille, i, j, val):
            grille[i][j] = val
            afficher_grille(grille, canvas, entrees)
            suivante_i, suivante_j = suivante(i, j)
            if suivante_i is not None and suivante_j is not None:
                entrees[suivante_i][suivante_j].focus()
        else:
            entrees[i][j].delete(0, tk.END)
    except ValueError:
        entrees[i][j].delete(0, tk.END)


def resoudre_grille(grille, canvas, entrees):
    """
    Résout la grille de Sudoku et l'affiche sur le canvas.
    """
    if resoudre(grille):
        afficher_grille(grille, canvas, entrees)
    else:
        print("Pas de solution trouvée")


def interface_sudoku():
    """
    Crée l'interface graphique pour jouer et résoudre un Sudoku.
    """
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Sudoku")

    # Création du canvas pour afficher la grille
    canvas = tk.Canvas(root, width=540, height=540)
    canvas.pack()

    # Exemple de grille
    grille = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    # Créer une matrice pour les entrées utilisateur
    entrees = [[None for _ in range(9)] for _ in range(9)]

    # Afficher la grille initiale
    afficher_grille(grille, canvas, entrees)

    # Bouton pour vérifier la saisie de l'utilisateur
    bouton_verifier = tk.Button(root, text="Vérifier",
                                command=lambda: [verifier_et_valider(grille, canvas, entrees, i, j) for i in range(9)
                                                 for j in range(9) if
                                                 entrees[i][j] is not None and entrees[i][j].get() != ""])
    bouton_verifier.pack()

    # Bouton pour résoudre la grille
    bouton_resoudre = tk.Button(root, text="Résoudre", command=lambda: resoudre_grille(grille, canvas, entrees))
    bouton_resoudre.pack()

    # Lancer la boucle principale de Tkinter
    root.mainloop()


if __name__ == "__main__":
    interface_sudoku()

# Fin du fichier sudoku.py
