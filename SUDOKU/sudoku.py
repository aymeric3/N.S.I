import tkinter as tk  # importe tkinter pour créer l'interface graphique
from tkinter import messagebox  # importe messagebox pour afficher des boîtes de dialogue
import random  # importe le module random pour générer des valeurs aléatoires

# génère une solution de sudoku
def generer_solution_sudoku():
    base = 3  # taille de la base du sudoku (3x3)
    cote = base * base  # taille de la grille complète (9x9)

    # fonction pour définir le motif de remplissage des cases
    def motif(r, c):
        return (base * (r % base) + r // base + c) % cote

    # mélange les éléments d'une liste
    def melanger(s):
        return random.sample(s, len(s))

    # mélange des lignes, colonnes et chiffres
    lignes = [g * base + r for g in melanger(range(base)) for r in melanger(range(base))]
    colonnes = [g * base + c for g in melanger(range(base)) for c in melanger(range(base))]
    chiffres = melanger(range(1, base * base + 1))  # mélange les chiffres de 1 à 9

    # crée la grille de sudoku
    grille = [[chiffres[motif(r, c)] for c in colonnes] for r in lignes]
    return grille

# démarre le jeu
def demarrer_jeu():
    cadre_demarrage.pack_forget()  # cache le menu de démarrage
    cadre_jeu.pack()  # affiche la grille de jeu
    afficher_sudoku()  # affiche la grille de sudoku
    cadre_controles.pack(pady=20)  # affiche les contrôles
    aller_premiere_case_vide()  # place le curseur sur la première case vide

# quitte le jeu avec confirmation
def quitter_jeu():
    if messagebox.askyesno("Confirmation", "êtes-vous sûr de vouloir quitter le jeu ?"):
        racine.destroy()  # ferme l'application si l'utilisateur confirme

# affiche la grille de sudoku
def afficher_sudoku():
    for r in range(9):  # parcourt chaque ligne
        for c in range(9):  # parcourt chaque colonne
            valeur = sudoku[r][c]  # obtient la valeur de la case
            case = tk.Entry(cadre_jeu, width=3, font=('Arial', 18), justify='center')  # crée une case de saisie
            case.grid(row=r, column=c, padx=2, pady=2)  # place la case dans la grille
            case.bind("<KeyRelease>", valider_saisie)  # associe la validation à chaque saisie
            if valeur != 0:  # si la case n'est pas vide (pré-remplie)
                case.insert(0, str(valeur))  # insère la valeur
                case.config(state='readonly')  # rend la case non modifiable
            cases[(r, c)] = case  # enregistre la case dans le dictionnaire

# valide la saisie de l'utilisateur
def valider_saisie(event):
    widget = event.widget  # récupère la case où l'utilisateur a écrit
    texte = widget.get()  # obtient le texte entré
    if len(texte) > 1 or not texte.isdigit() or not (1 <= int(texte) <= 9):  # vérifie si la saisie est incorrecte
        widget.delete(0, tk.END)  # efface la saisie si elle est incorrecte

# obtient la case actuellement sélectionnée
def obtenir_case_selectionnee():
    for (r, c), case in cases.items():  # parcourt chaque case
        if case == racine.focus_get():  # si la case a le focus
            return r, c  # retourne les coordonnées
    return None, None  # retourne None si aucune case n'est sélectionnée

# va à la première case vide
def aller_premiere_case_vide():
    for r in range(9):  # parcourt chaque ligne
        for c in range(9):  # parcourt chaque colonne
            if cases[(r, c)].get() == '':  # si la case est vide
                cases[(r, c)].focus_set()  # place le focus
                return

# donne un indice en remplissant une case vide
def donner_indice():
    row, col = obtenir_case_selectionnee()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None and sudoku[row][col] == 0:  # si une case vide est sélectionnée
        cases[(row, col)].insert(0, str(solution_sudoku[row][col]))  # insère la solution
        cases[(row, col)].config(state='readonly', disabledforeground='green')  # rend la case non modifiable et en vert

# vérifie si la grille est correcte
def verifier_grille():
    erreurs = False  # initialise le compteur d'erreurs
    for r in range(9):  # parcourt chaque ligne
        for c in range(9):  # parcourt chaque colonne
            case_valeur = cases[(r, c)].get()  # obtient la valeur entrée par l'utilisateur
            if case_valeur != str(solution_sudoku[r][c]):  # compare avec la solution
                cases[(r, c)].config(fg="red")  # met la case en rouge si incorrecte
                erreurs = True  # indique qu'il y a des erreurs
            else:
                cases[(r, c)].config(fg="black")  # remet la couleur en noir si correcte
    if not erreurs:  # si aucune erreur n'a été trouvée
        messagebox.showinfo("Victoire", "Félicitations ! Vous avez complété le Sudoku.")  # affiche le message de victoire

# configuration de la fenêtre principale
racine = tk.Tk()  # crée la fenêtre principale
racine.title("Jeu de Sudoku")  # titre de la fenêtre
racine.geometry("500x650")  # taille de la fenêtre
racine.resizable(False, False)  # empêche le redimensionnement

# interface de démarrage
cadre_demarrage = tk.Frame(racine)  # crée le cadre de démarrage
tk.Label(cadre_demarrage, text="Bienvenue dans le Sudoku", font=('Arial', 18, 'bold')).pack(pady=20)  # titre
tk.Button(cadre_demarrage, text="Démarrer", command=demarrer_jeu, font=('Arial', 14, "bold"), width=15, bg='#4CAF50', fg='white').pack(pady=10)  # bouton démarrer
tk.Button(cadre_demarrage, text="Quitter", command=quitter_jeu, font=('Arial', 14, "bold"), width=15, bg='#F44336', fg='white').pack(pady=10)  # bouton quitter
cadre_demarrage.pack(expand=True)  # affiche le cadre de démarrage

# interface de jeu
cadre_jeu = tk.Frame(racine)  # crée le cadre de jeu
cases = {}  # dictionnaire pour les cases de la grille
solution_sudoku = generer_solution_sudoku()  # génère une solution de sudoku
sudoku = [[0 if random.random() < 0.5 else num for num in row] for row in solution_sudoku]  # grille partiellement remplie

# boutons de contrôle
cadre_controles = tk.Frame(racine)  # crée le cadre pour les contrôles
tk.Button(cadre_controles, text="Vérifier", command=verifier_grille, font=('Arial', 14)).pack(pady=5)  # bouton vérifier
tk.Button(cadre_controles, text="Indice", command=donner_indice, font=('Arial', 14)).pack(pady=5)  # bouton indice
tk.Button(cadre_controles, text="Abandonner", command=quitter_jeu, font=('Arial', 14), bg="red", fg="white").pack(pady=5)  # bouton abandonner

racine.mainloop()  # lance la boucle principale de l'application
