# sudoku.py
import tkinter as tk
from tkinter import messagebox
import copy
from fonctions_eleve_1 import ligne, colonne, bloc
from fonctions_eleve_2 import suivante
from fonctions_eleve_3 import grille_complete
from fonctions_eleve_4 import resoudre

def interface_sudoku():
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

    # On crée une copie de la grille et on la résout pour obtenir la solution
    solution = copy.deepcopy(grille)
    resoudre(solution)

    # Créer une matrice pour les entrées utilisateur
    entrees = [[None for _ in range(9)] for _ in range(9)]

    def afficher_grille():
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
                    entrees[i][j].bind("<Return>", lambda e, i=i, j=j: verifier_valeur_cell(i, j))
                    entrees[i][j].bind("<KeyRelease>", filtrer_entree)

    def filtrer_entree(event):
        """
        Empêche la saisie de caractères non numériques ou de chiffres en dehors de 1-9.
        """
        widget = event.widget
        valeur = widget.get()
        if not valeur.isdigit() or not (1 <= int(valeur) <= 9):
            widget.delete(0, tk.END)

    def verifier_valeur_cell(i, j):
        """
        Vérifie la valeur entrée dans la case (i, j).
        """
        try:
            val = int(entrees[i][j].get())
            if val in range(1, 10):
                # Vérifier si la valeur est possible selon les règles du Sudoku
                if val not in ligne(grille, i) and val not in colonne(grille, j) and val not in bloc(grille, i, j):
                    # La valeur est correcte selon les règles
                    entrees[i][j].config(state='readonly')
                    grille[i][j] = val  # Met à jour la grille avec la valeur correcte
                    # Déplace le curseur vers la prochaine case vide
                    suivante_i, suivante_j = suivante(i, j)
                    while suivante_i < 9:
                        if grille[suivante_i][suivante_j] == 0:
                            entrees[suivante_i][suivante_j].focus_set()
                            break
                        suivante_i, suivante_j = suivante(suivante_i, suivante_j)
                    else:
                        # Toutes les cases sont remplies
                        if grille_complete(grille):
                            messagebox.showinfo("Félicitations", "Vous avez résolu le Sudoku !")
                    return
                else:
                    # Valeur incorrecte selon les règles du Sudoku
                    entrees[i][j].delete(0, tk.END)
                    entrees[i][j].focus_set()
            else:
                # Valeur hors limites
                entrees[i][j].delete(0, tk.END)
                entrees[i][j].focus_set()
        except ValueError:
            entrees[i][j].delete(0, tk.END)
            entrees[i][j].focus_set()

    def obtenir_case_selectionnee():
        """
        Obtient les coordonnées de la case actuellement sélectionnée.
        """
        focused_widget = root.focus_get()
        for i in range(9):
            for j in range(9):
                if entrees[i][j] == focused_widget:
                    return i, j
        return None, None

    def verifier_valeur():
        """
        Vérifie la valeur de la case sélectionnée lorsque le bouton est pressé.
        """
        i, j = obtenir_case_selectionnee()
        if i is not None and j is not None:
            verifier_valeur_cell(i, j)

    # Afficher la grille initiale
    afficher_grille()

    # Bouton pour vérifier la saisie de l'utilisateur
    bouton_verifier = tk.Button(root, text="Vérifier", command=verifier_valeur)
    bouton_verifier.pack(pady=10)

    # Lancer la boucle principale de Tkinter
    root.mainloop()


if __name__ == "__main__":
    interface_sudoku()

# Fin du fichier sudoku.py
