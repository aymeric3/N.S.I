import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# générer une solution de Sudoku (exemple simple avec une grille partiellement remplie)
def generer_solution_sudoku():
    base = 3  # taille de la base du sudoku (3x3)
    cote = base * base  # taille de la grille complète (9x9)
    def motif(r, c): return (base*(r % base) + r//base + c) % cote  # fonction pour définir le motif de remplissage des cases
    def melanger(s): return random.sample(s, len(s))  # fonction qui mélange les éléments d'une liste
    lignes = [g*base + r for g in melanger(range(base)) for r in melanger(range(base))]  # mélange des lignes
    colonnes = [g*base + c for g in melanger(range(base)) for c in melanger(range(base))]  # mélange des colonnes
    chiffres = melanger(range(1, base*base + 1))  # mélange des chiffres de 1 à 9
    grille = [[chiffres[motif(r, c)] for c in colonnes] for r in lignes]  # création de la grille remplie avec les chiffres mélangés
    return grille

# fonctions pour démarrer et quitter le jeu
def demarrer_jeu():
    cadre_demarrage.pack_forget()  # cache le menu de démarrage
    etiquette_fond.place_forget()  # retire l'image d'arrière-plan
    cadre_jeu.pack()  # affiche la grille de jeu
    afficher_sudoku()  # affiche la grille de Sudoku
    cadre_controles.pack(pady=20)  # affiche les contrôles (boutons sous la grille)
    aller_premiere_case_vide()  # place le curseur sur la première case vide

def quitter_jeu():
    if messagebox.askyesno("Confirmation", "êtes-vous sûr de vouloir quitter le jeu ?"):
        racine.destroy()  # ferme l'application si confirmation positive

# fonction pour afficher la grille de Sudoku
def afficher_sudoku():
    for r in range(9):  # boucle sur chaque ligne
        for c in range(9):  # boucle sur chaque colonne
            valeur = sudoku[r][c]  # obtient la valeur de chaque case
            case = tk.Entry(cadre_jeu, width=3, font=('Arial', 18), justify='center')  # crée une case de saisie
            case.grid(row=r, column=c, padx=2, pady=2)  # place la case dans la grille
            case.bind("<KeyRelease>", valider_saisie)  # associe la validation des entrées à chaque saisie
            if valeur != 0:  # si la valeur n'est pas 0 (case pré-remplie)
                case.insert(0, str(valeur))  # insère la valeur dans la case
                case.config(state='readonly')  # rend la case non modifiable
            cases[(r, c)] = case  # enregistre la référence de la case dans un dictionnaire

# fonction pour valider la valeur entrée par l'utilisateur
def valider_saisie(event):
    widget = event.widget  # récupère la case où l'utilisateur a écrit
    texte = widget.get()  # obtient le texte entré
    if len(texte) > 1 or not texte.isdigit() or not (1 <= int(texte) <= 9):  # si la saisie est incorrecte (pas un chiffre entre 1 et 9)
        widget.delete(0, tk.END)  # efface la saisie

# fonction pour obtenir la case actuellement sélectionnée
def obtenir_case_selectionnee():
    for (r, c), case in cases.items():  # boucle sur chaque case
        if case == racine.focus_get():  # si la case a le focus
            return r, c  # retourne les coordonnées de la case
    return None, None  # retourne None si aucune case n'est sélectionnée

# fonction pour aller à la première case vide
def aller_premiere_case_vide():
    for r in range(9):  # boucle sur chaque ligne
        for c in range(9):  # boucle sur chaque colonne
            if cases[(r, c)].get() == '':  # si la case est vide
                cases[(r, c)].focus_set()  # place le focus sur la première case vide
                return

# fonction pour se déplacer vers la prochaine case vide dans la région 3x3
def aller_prochaine_case_vide_region(row, col):
    region_ligne, region_colonne = row // 3 * 3, col // 3 * 3  # calcule la région 3x3 correspondante
    for r in range(region_ligne, region_ligne + 3):  # boucle sur chaque ligne de la région
        for c in range(region_colonne, region_colonne + 3):  # boucle sur chaque colonne de la région
            if cases[(r, c)].get() == '':  # si la case est vide
                cases[(r, c)].focus_set()  # place le focus sur la case
                return

# fonction pour se déplacer vers la prochaine case vide dans la région suivante
def aller_prochaine_case_vide_region_suivante(region_ligne, region_colonne):
    prochaine_region_ligne = (region_ligne + 3) % 9 if region_ligne + 3 < 9 else 0  # calcule la prochaine région ligne
    prochaine_region_colonne = region_colonne if prochaine_region_ligne != 0 else (region_colonne + 3) % 9  # calcule la prochaine région colonne
    for r in range(prochaine_region_ligne, prochaine_region_ligne + 3):  # boucle sur chaque ligne de la prochaine région
        for c in range(prochaine_region_colonne, prochaine_region_colonne + 3):  # boucle sur chaque colonne de la prochaine région
            if cases[(r, c)].get() == '':  # si la case est vide
                cases[(r, c)].focus_set()  # place le focus sur la case
                return

# fonction pour donner un indice à l'utilisateur (remplir une case vide)
def donner_indice():
    row, col = obtenir_case_selectionnee()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None:  # si une case est sélectionnée
        region_ligne, region_colonne = row // 3 * 3, col // 3 * 3  # calcule la région 3x3 correspondante
        for r in range(region_ligne, region_ligne + 3):  # boucle sur chaque ligne de la région
            for c in range(region_colonne, region_colonne + 3):  # boucle sur chaque colonne de la région
                if (r, c) in cases and cases[(r, c)].get() == '':  # si la case est vide
                    case = cases[(r, c)]
                    case.delete(0, tk.END)  # efface le contenu de la case
                    case.insert(0, str(solution_sudoku[r][c]))  # insère la solution dans la case
                    case.config(state='readonly', disabledforeground='green')  # affiche l'indice en vert
                    aller_prochaine_case_vide_region(region_ligne, region_colonne)  # déplace le focus vers la prochaine case vide
                    return
        aller_prochaine_case_vide_region(region_ligne, region_colonne)  # déplace le focus si aucune case vide n'a été trouvée
        verifier_victoire()  # vérifie si la partie est gagnée
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner une case.")  # affiche un message d'erreur si aucune case n'est sélectionnée

# fonction pour donner un indice pour toute une région 3x3
def donner_indice_region():
    row, col = obtenir_case_selectionnee()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None:  # si une case est sélectionnée
        region_ligne, region_colonne = row // 3 * 3, col // 3 * 3  # calcule la région 3x3 correspondante
        for r in range(region_ligne, region_ligne + 3):  # boucle sur chaque ligne de la région
            for c in range(region_colonne, region_colonne + 3):  # boucle sur chaque colonne de la région
                if (r, c) in cases and cases[(r, c)].get() == '':  # si la case est vide
                    case = cases[(r, c)]
                    case.delete(0, tk.END)  # efface le contenu de la case
                    case.insert(0, str(solution_sudoku[r][c]))  # insère la solution dans la case
                    case.config(state='readonly', disabledforeground='orange')  # affiche l'indice en orange
        aller_prochaine_case_vide_region_suivante(region_ligne, region_colonne)  # déplace le focus vers la prochaine région
        verifier_victoire()  # vérifie si la partie est gagnée
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner une case.")  # affiche un message d'erreur si aucune case n'est sélectionnée

# fonction pour vérifier si la valeur entrée est correcte
def verifier_valeur():
    row, col = obtenir_case_selectionnee()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None:  # si une case est sélectionnée
        valeur = cases[(row, col)].get()  # obtient la valeur de la case
        if valeur.isdigit() and int(valeur) == solution_sudoku[row][col]:  # si la valeur est correcte
            messagebox.showinfo("Résultat", "La valeur est correcte !")  # affiche un message de confirmation
            cases[(row, col)].config(state='readonly', disabledforeground='blue')  # affiche en bleu si la valeur est correcte
            aller_prochaine_case_vide_region(row, col)  # déplace le focus vers la prochaine case vide
            verifier_victoire()  # vérifie si la partie est gagnée
        else:
            messagebox.showwarning("Résultat", "La valeur est incorrecte.")  # affiche un message d'avertissement si la valeur est incorrecte
            cases[(row, col)].delete(0, tk.END)  # efface la valeur incorrecte
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner une case.")  # affiche un message d'erreur si aucune case n'est sélectionnée

# fonction pour vérifier si le joueur a gagné
def verifier_victoire():
    for (r, c), case in cases.items():  # boucle sur chaque case
        if case.get() == '' or case.get() != str(solution_sudoku[r][c]):  # si une case est vide ou incorrecte
            return  # retourne sans rien faire
    if messagebox.askyesno("Victoire", "Félicitations ! Vous avez complété le Sudoku. Voulez-vous recommencer une nouvelle partie ?"):
        redemarrer_jeu()  # redémarre une nouvelle partie si l'utilisateur accepte
    else:
        quitter_jeu()  # quitte le jeu sinon

# fonction pour redémarrer une nouvelle partie
def redemarrer_jeu():
    global solution_sudoku, sudoku, cases
    solution_sudoku = generer_solution_sudoku()  # génère une nouvelle solution de Sudoku
    sudoku = [[0 if random.random() < 0.5 else num for num in row] for row in solution_sudoku]  # crée une grille partiellement remplie
    cases.clear()  # efface les anciennes entrées
    for widget in cadre_jeu.winfo_children():
        widget.destroy()  # efface la grille actuelle
    afficher_sudoku()  # affiche la nouvelle grille
    aller_premiere_case_vide()  # place le focus sur la première case vide

# interface principale
racine = tk.Tk()  # crée la fenêtre principale
racine.title("Jeu de Sudoku")  # titre de la fenêtre
racine.geometry("500x650")  # taille de la fenêtre
racine.resizable(False, False)  # rend la fenêtre non redimensionnable

# image d'arrière-plan pour le menu de démarrage
image_fond = Image.open("fond_start.jpg")  # remplacer par le chemin de votre image
image_fond = image_fond.resize((1000, 700))  # redimensionne l'image d'arrière-plan
photo_fond = ImageTk.PhotoImage(image_fond)
etiquette_fond = tk.Label(racine, image=photo_fond)  # crée un label avec l'image d'arrière-plan
etiquette_fond.place(x=0, y=0, relwidth=1, relheight=1)  # place l'image d'arrière-plan

# démarrage du jeu
cadre_demarrage = tk.Frame(racine, bg='white')  # crée le cadre pour le menu de démarrage
tk.Label(cadre_demarrage, text="Bienvenue dans le Sudoku", font=('Arial', 18, 'bold'), bg='white').pack(pady=20)  # texte d'accueil
tk.Button(cadre_demarrage, text="Démarrer", command=demarrer_jeu, font=('Arial', 14, "bold", "italic"), width=15, bg='#4CAF50', fg='white').pack(pady=10)  # bouton pour démarrer le jeu
tk.Button(cadre_demarrage, text="Quitter", command=quitter_jeu, font=('Arial', 14, "bold", "italic"), width=15, bg='#F44336', fg='white').pack(pady=10)  # bouton pour quitter le jeu
cadre_demarrage.pack(expand=True)  # affiche le cadre de démarrage

# jeu de Sudoku
cadre_jeu = tk.Frame(racine)  # crée le cadre pour le jeu
cases = {}  # dictionnaire pour stocker les entrées de chaque case
solution_sudoku = generer_solution_sudoku()  # génère une solution de Sudoku
sudoku = [[0 if random.random() < 0.5 else num for num in row] for row in solution_sudoku]  # crée une grille partiellement remplie

# boutons sous la grille (contrôles du jeu)
cadre_controles = tk.Frame(racine)  # crée le cadre pour les boutons de contrôle

# bouton pour vérifier une case, centré
bouton_verifier = tk.Button(cadre_controles, text="Vérifier", command=verifier_valeur, font=('Arial', 18, "bold"))
bouton_verifier.pack(pady=10)

# cadre pour les boutons d'indice, placés l'un à côté de l'autre
cadre_indices = tk.Frame(cadre_controles)
tk.Button(cadre_indices, text="Indice pour case", command=donner_indice, font=('Arial', 10, "italic"), bg="green", fg="white").pack(side='left', padx=5, pady=10)  # bouton pour donner un indice pour une case
tk.Button(cadre_indices, text="Indice pour 3x3", command=donner_indice_region, font=('Arial', 10, "italic"), bg="green", fg="white").pack(side='left', padx=5, pady=10)  # bouton pour donner un indice pour une région 3x3
cadre_indices.pack()

# bouton pour quitter le jeu, placé en bas
bouton_quitter = tk.Button(cadre_controles, text="Abandonner", command=quitter_jeu, font=('Arial', 12), bg='red', fg='white')
bouton_quitter.pack(pady=10)

cadre_jeu.pack(pady=10)  # affiche le cadre de jeu

racine.mainloop()  # lance la boucle principale de l'application
