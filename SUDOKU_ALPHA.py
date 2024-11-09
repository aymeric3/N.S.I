import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# générer une solution de Sudoku (exemple simple avec une grille partiellement remplie)
def generate_sudoku_solution():
    base = 3  # taille de la base du sudoku (3x3)
    side = base * base  # taille de la grille complète (9x9)
    def pattern(r, c): return (base*(r % base) + r//base + c) % side  # fonction pour définir le motif de remplissage des cases
    def shuffle(s): return random.sample(s, len(s))  # fonction qui mélange les éléments d'une liste
    rows = [g*base + r for g in shuffle(range(base)) for r in shuffle(range(base))]  # mélange des lignes
    cols = [g*base + c for g in shuffle(range(base)) for c in shuffle(range(base))]  # mélange des colonnes
    nums = shuffle(range(1, base*base + 1))  # mélange des chiffres de 1 à 9
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]  # création de la grille remplie avec les chiffres mélangés
    return board

# fonctions pour démarrer et quitter le jeu
def start_game():
    start_frame.pack_forget()  # cache le menu de démarrage
    background_label.place_forget()  # retire l'image d'arrière-plan
    game_frame.pack()  # affiche la grille de jeu
    display_sudoku()  # affiche la grille de Sudoku
    control_frame.pack(pady=20)  # affiche les contrôles (boutons sous la grille)
    move_to_first_empty_cell()  # place le curseur sur la première case vide

def quit_game():
    if messagebox.askyesno("Confirmation", "êtes-vous sûr de vouloir quitter le jeu ?"):
        root.destroy()  # ferme l'application si confirmation positive

# fonction pour afficher la grille de Sudoku
def display_sudoku():
    for r in range(9):  # boucle sur chaque ligne
        for c in range(9):  # boucle sur chaque colonne
            value = sudoku[r][c]  # obtient la valeur de chaque case
            entry = tk.Entry(game_frame, width=3, font=('Arial', 18), justify='center')  # crée une case de saisie
            entry.grid(row=r, column=c, padx=2, pady=2)  # place la case dans la grille
            entry.bind("<KeyRelease>", validate_entry)  # associe la validation des entrées à chaque saisie
            if value != 0:  # si la valeur n'est pas 0 (case pré-remplie)
                entry.insert(0, str(value))  # insère la valeur dans la case
                entry.config(state='readonly')  # rend la case non modifiable
            entries[(r, c)] = entry  # enregistre la référence de la case dans un dictionnaire

# fonction pour valider la valeur entrée par l'utilisateur
def validate_entry(event):
    widget = event.widget  # récupère la case où l'utilisateur a écrit
    text = widget.get()  # obtient le texte entré
    if len(text) > 1 or not text.isdigit() or not (1 <= int(text) <= 9):  # si la saisie est incorrecte (pas un chiffre entre 1 et 9)
        widget.delete(0, tk.END)  # efface la saisie

# fonction pour obtenir la case actuellement sélectionnée
def get_selected_cell():
    for (r, c), entry in entries.items():  # boucle sur chaque case
        if entry == root.focus_get():  # si la case a le focus
            return r, c  # retourne les coordonnées de la case
    return None, None  # retourne None si aucune case n'est sélectionnée

# fonction pour se déplacer vers la première case vide
def move_to_first_empty_cell():
    for r in range(9):  # boucle sur chaque ligne
        for c in range(9):  # boucle sur chaque colonne
            if entries[(r, c)].get() == '':  # si la case est vide
                entries[(r, c)].focus_set()  # place le focus sur la première case vide
                return

# fonction pour se déplacer à la prochaine case vide dans la région 3x3
def move_to_next_empty_cell_within_region(row, col):
    region_row, region_col = row // 3 * 3, col // 3 * 3  # calcule la région 3x3 correspondante
    for r in range(region_row, region_row + 3):  # boucle sur chaque ligne de la région
        for c in range(region_col, region_col + 3):  # boucle sur chaque colonne de la région
            if entries[(r, c)].get() == '':  # si la case est vide
                entries[(r, c)].focus_set()  # place le focus sur la case
                return

# fonction pour se déplacer à la prochaine case vide dans la région suivante
def move_to_next_empty_cell_in_next_region(region_row, region_col):
    next_region_row = (region_row + 3) % 9 if region_row + 3 < 9 else 0  # calcule la prochaine région ligne
    next_region_col = region_col if next_region_row != 0 else (region_col + 3) % 9  # calcule la prochaine région colonne
    for r in range(next_region_row, next_region_row + 3):  # boucle sur chaque ligne de la prochaine région
        for c in range(next_region_col, next_region_col + 3):  # boucle sur chaque colonne de la prochaine région
            if entries[(r, c)].get() == '':  # si la case est vide
                entries[(r, c)].focus_set()  # place le focus sur la case
                return

# fonction pour donner un indice à l'utilisateur (remplir une case vide)
def give_hint():
    row, col = get_selected_cell()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None:  # si une case est sélectionnée
        region_row, region_col = row // 3 * 3, col // 3 * 3  # calcule la région 3x3 correspondante
        for r in range(region_row, region_row + 3):  # boucle sur chaque ligne de la région
            for c in range(region_col, region_col + 3):  # boucle sur chaque colonne de la région
                if (r, c) in entries and entries[(r, c)].get() == '':  # si la case est vide
                    entry = entries[(r, c)]
                    entry.delete(0, tk.END)  # efface le contenu de la case
                    entry.insert(0, str(sudoku_solution[r][c]))  # insère la solution dans la case
                    entry.config(state='readonly', disabledforeground='green')  # affiche l'indice en vert
                    move_to_next_empty_cell_within_region(region_row, region_col)  # déplace le focus vers la prochaine case vide
                    return
        move_to_next_empty_cell_within_region(region_row, region_col)  # déplace le focus si aucune case vide n'a été trouvée
        check_win()  # vérifie si la partie est gagnée
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner une case.")  # affiche un message d'erreur si aucune case n'est sélectionnée

# fonction pour donner un indice pour toute une région 3x3
def give_region_hint():
    row, col = get_selected_cell()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None:  # si une case est sélectionnée
        region_row, region_col = row // 3 * 3, col // 3 * 3  # calcule la région 3x3 correspondante
        for r in range(region_row, region_row + 3):  # boucle sur chaque ligne de la région
            for c in range(region_col, region_col + 3):  # boucle sur chaque colonne de la région
                if (r, c) in entries and entries[(r, c)].get() == '':  # si la case est vide
                    entry = entries[(r, c)]
                    entry.delete(0, tk.END)  # efface le contenu de la case
                    entry.insert(0, str(sudoku_solution[r][c]))  # insère la solution dans la case
                    entry.config(state='readonly', disabledforeground='orange')  # affiche l'indice en orange
        move_to_next_empty_cell_in_next_region(region_row, region_col)  # déplace le focus vers la prochaine région
        check_win()  # vérifie si la partie est gagnée
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner une case.")  # affiche un message d'erreur si aucune case n'est sélectionnée

# fonction pour vérifier si la valeur entrée est correcte
def check_value():
    row, col = get_selected_cell()  # obtient la case actuellement sélectionnée
    if row is not None and col is not None:  # si une case est sélectionnée
        value = entries[(row, col)].get()  # obtient la valeur de la case
        if value.isdigit() and int(value) == sudoku_solution[row][col]:  # si la valeur est correcte
            messagebox.showinfo("Résultat", "La valeur est correcte !")  # affiche un message de confirmation
            entries[(row, col)].config(state='readonly', disabledforeground='blue')  # affiche en bleu si la valeur est correcte
            move_to_next_empty_cell_within_region(row, col)  # déplace le focus vers la prochaine case vide
            check_win()  # vérifie si la partie est gagnée
        else:
            messagebox.showwarning("Résultat", "La valeur est incorrecte.")  # affiche un message d'avertissement si la valeur est incorrecte
            entries[(row, col)].delete(0, tk.END)  # efface la valeur incorrecte
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner une case.")  # affiche un message d'erreur si aucune case n'est sélectionnée

# fonction pour vérifier si le joueur a gagné
def check_win():
    for (r, c), entry in entries.items():  # boucle sur chaque case
        if entry.get() == '' or entry.get() != str(sudoku_solution[r][c]):  # si une case est vide ou incorrecte
            return  # retourne sans rien faire
    if messagebox.askyesno("Victoire", "Félicitations ! Vous avez complété le Sudoku. Voulez-vous recommencer une nouvelle partie ?"):
        restart_game()  # redémarre une nouvelle partie si l'utilisateur accepte
    else:
        quit_game()  # quitte le jeu sinon

# fonction pour redémarrer une nouvelle partie
def restart_game():
    global sudoku_solution, sudoku, entries
    sudoku_solution = generate_sudoku_solution()  # génère une nouvelle solution de Sudoku
    sudoku = [[0 if random.random() < 0.5 else num for num in row] for row in sudoku_solution]  # crée une grille partiellement remplie
    entries.clear()  # efface les anciennes entrées
    for widget in game_frame.winfo_children():
        widget.destroy()  # efface la grille actuelle
    display_sudoku()  # affiche la nouvelle grille
    move_to_first_empty_cell()  # place le focus sur la première case vide

# interface principale
root = tk.Tk()  # crée la fenêtre principale
root.title("Jeu de Sudoku")  # titre de la fenêtre
root.geometry("500x650")  # taille de la fenêtre
root.resizable(False, False)  # rend la fenêtre non redimensionnable

# image d'arrière-plan pour le menu de démarrage
background_image = Image.open("fond_start.jpg")  # remplacer par le chemin de votre image
background_image = background_image.resize((1000, 700))  # redimensionne l'image d'arrière-plan
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)  # crée un label avec l'image d'arrière-plan
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # place l'image d'arrière-plan

# démarrage du jeu
start_frame = tk.Frame(root, bg='white')  # crée le cadre pour le menu de démarrage
tk.Label(start_frame, text="Bienvenue dans le Sudoku", font=('Arial', 18, 'bold'), bg='white').pack(pady=20)  # texte d'accueil
tk.Button(start_frame, text="Démarrer", command=start_game, font=('Arial', 14, "bold", "italic"), width=15, bg='#4CAF50', fg='white').pack(pady=10)  # bouton pour démarrer le jeu
tk.Button(start_frame, text="Quitter", command=quit_game, font=('Arial', 14, "bold", "italic"), width=15, bg='#F44336', fg='white').pack(pady=10)  # bouton pour quitter le jeu
start_frame.pack(expand=True)  # affiche le cadre de démarrage

# jeu de Sudoku
game_frame = tk.Frame(root)  # crée le cadre pour le jeu
entries = {}  # dictionnaire pour stocker les entrées de chaque case
sudoku_solution = generate_sudoku_solution()  # génère une solution de Sudoku
sudoku = [[0 if random.random() < 0.5 else num for num in row] for row in sudoku_solution]  # crée une grille partiellement remplie

# boutons sous la grille (contrôles du jeu)
control_frame = tk.Frame(root)  # crée le cadre pour les boutons de contrôle

# bouton pour vérifier une case, centré
check_button = tk.Button(control_frame, text="Vérifier", command=check_value, font=('Arial', 18, "bold"))
check_button.pack(pady=10)

# cadre pour les boutons d'indice, placés l'un à côté de l'autre
hint_frame = tk.Frame(control_frame)
tk.Button(hint_frame, text="Indice pour case", command=give_hint, font=('Arial', 10, "italic"), bg = "green", fg = "white").pack(side='left', padx=5, pady=10)  # bouton pour donner un indice pour une case
tk.Button(hint_frame, text="Indice pour 3x3", command=give_region_hint, font=('Arial', 10, "italic"), bg = "green", fg = "white").pack(side='left', padx=5, pady=10)  # bouton pour donner un indice pour une région 3x3
hint_frame.pack()

# bouton pour quitter le jeu, placé en bas
quit_button = tk.Button(control_frame, text="Abandonner", command=quit_game, font=('Arial', 12), bg='red', fg = 'white')
quit_button.pack(pady=10)

game_frame.pack(pady=10)  # affiche le cadre de jeu

root.mainloop()  # lance la boucle principale de l'application
