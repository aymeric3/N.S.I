import random
import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk

def charger(filename:str)->list : # Cette fonction permet de lire le résultat du fichier et le stocke sous forme de liste.
    resultat = []
    with open(filename, 'r') as fichier:
        for ligne in fichier:
            resultat.append(ligne.rstrip().upper())
    return resultat
def init_grid(): # cette fonction initialise la grille avec la première case de la première ligne
    for i in range(6):  # 6 essais possibles
        row = []
        for j in range(len(mot)):  # Longueur du mot
            ent = tk.Entry(frame, font=('Helvetica', 20), width=2, justify='center', borderwidth=2, relief="ridge", bg="#147cbc")
            ent.grid(row=i, column=j, padx=5, pady=5) # .grid sert à insérer la valeur dans la grille et la configurer (taille etc)
            if i == 0 and j == 0:  # Première lettre toujours révélée pour le premier essai
                ent.insert(0, mot[0]) #.insert sert à insérer une valeur dans une case
                ent.config(state='readonly', readonlybackground='#dc5444', fg='white') #.config sert à configurer la case (couleur etc)
            row.append(ent)
        grid.append(row)

def clear_grid(): #cette fonction sert à vider les cases
    for ligne in grid:
        for case in ligne:
            case.destroy()
    grid.clear()
def setup_entries(): # cette fonction sert à permettre de configurer les entrées
    for i in range(6):
        for j in range(len(mot)):
            grid[i][j].bind('<KeyRelease>', lambda e, x=i, y=j: gerer_entree_lettre(x, y)) #KeyRelease est un évènement qui se produit lorsque une touche est relachée après l'avoir pressée
            # et .bind sert à lire l'évènement KeyRelease à chaque case, et chaque case est lié à cette évènement.

def gerer_entree_lettre(i, j): # cette fonction sert à mettre le curseur soit à la case d'après soit à la ligne d'après, elle fait le focus grâce à "focus_set)"
    current_entry = grid[i][j]
    entree_lettre = current_entry.get().upper()
    current_entry.delete(0, tk.END)
    current_entry.insert(0, entree_lettre)
    if len(current_entry.get()) > 0:
        current_entry.delete(1, tk.END)
    next_col = j + 1
    if next_col < len(mot):
        grid[i][next_col].focus_set()
    elif next_col == len(mot) and i < 5:
        grid[i+1][1].focus_set()

def verifier_mot(): # cette fonction contient les règles du jeu pour vérifier si le mot est bon ou pas et si le nombre de lettre suffisant a été rentré.
    global tries
    saisie = ''.join([entry.get().upper() for entry in grid[tries]])
    if len(saisie) != len(mot) or ' ' in saisie:
        messagebox.showinfo("Erreur", "Vous devez remplir toutes les cases avant de soumettre.")
        return False

    lettres_restantes = {lettre: mot.count(lettre) for lettre in set(mot)}

    # Marquer les correctes
    for idx, lettre in enumerate(saisie):
        if lettre == mot[idx]:
            grid[tries][idx].config(bg='#dc5444')
            lettres_restantes[lettre] -= 1

    # Marquer les mal placées ou incorrectes
    for idx, lettre in enumerate(saisie):
        if grid[tries][idx]['bg'] != '#dc5444':  # Ne vérifier que les cases non rouges
            if lettre in mot and lettres_restantes[lettre] > 0:
                grid[tries][idx].config(bg='#e9c244')
                lettres_restantes[lettre] -= 1
            else:
                grid[tries][idx].config(bg='#147cbc')

    # Vérifier si le mot est trouvé
    if saisie == mot:
        messagebox.showinfo("Jeu Motus", "Félicitations, vous avez trouvé le mot!") #.showinfo sert à afficher un titre et un message, en gros afficher une information
        return True
    return False

def fin_du_jeu(message): # cette fonction sert à afficher une fenêtre avec un message et 2 boutons "Oui" et "Non" pour avoir le choix de rejouer ou pas.
    fenetre = Toplevel(root)
    fenetre.title("REJOUER ?")
    tk.Label(fenetre, text=message, font= ("Helvetica", 16)).pack(pady = 12)
    tk.Button(fenetre, text="Oui", command=lambda:[fenetre.destroy(), reset_game()], font= ("Helvetica", 16), bg = "white", fg = "black", borderwidth= 4).pack(pady = 12)
    tk.Button(fenetre, text="Non", command=lambda:[fenetre.destroy(), abandonner()], font=("Helvetica", 16), bg="white", fg="black", borderwidth= 4).pack(pady=12)
def jouer(): #la fonction jouer sert à contrôler le jeu si on win ou lose et de préparer une nouvelle tentative ou arrêter le jeu
    if verifier_mot():
        fin_du_jeu("Félicitations, vous avez trouvé le mot!\n\nSouhaitez-vous rejouer ?")

        return
    if tries < 5:
        préparer_nouvelle_tentative()
    else:
        fin_du_jeu(f"Vous avez perdu ! Le mot était : {mot}\n\nSouhaitez-vous rejouer ?")

def préparer_nouvelle_tentative(): # cette fonction permet de préparer une nouvelle ligne et rempli la première case pour chaque ligne par le premier caractère
    global tries
    tries += 1
    if tries < 6:
        for idx in range(len(mot)):
            current_entry = grid[tries - 1][idx]
            next_entry = grid[tries][idx]
            if idx == 0:
                next_entry.delete(0, tk.END)
                next_entry.insert(0, mot[0])
                next_entry.config(state='readonly', readonlybackground='#dc5444', fg='white')
            else:
                next_entry.config(state='normal', bg='#147cbc', fg='black')
                if current_entry['bg'] == '#dc5444': # Si correctement placée dans l'essai précédent
                    next_entry.delete(0, tk.END)
                    next_entry.insert(0, current_entry.get())
                    next_entry.config(state='readonly', readonlybackground='#dc5444', fg='white')
        grid[tries][1].focus_set()  # Focus sur la première case modifiable de la ligne suivante


def reset_game(): # cette fonction sert à relancer le jeu et s'assure également de réinitialiser la grille
    global tries, mot
    tries = 0
    mot = random.choice(dico).upper()
    clear_grid()
    init_grid()
    setup_entries()
    for row in grid:
        for entry in row: #row signifie ligne
            entry.config(state='normal', bg='#147cbc', fg='black')
            entry.delete(0, tk.END)
    grid[0][0].insert(0, mot[0])
    grid[0][0].config(state='readonly', readonlybackground='#dc5444', fg='white')
    for i in range(1, len(mot)):
        grid[0][i].config(state='normal', bg='#147cbc', fg='black')
    grid[0][1].focus_set() if len(mot) > 1 else None

def fenetre_du_jeu(): # cette fonction sert à lancer la fenêtre du jeu
    global root, frame, mot, grid, tries, dico

    root = tk.Tk()
    root.title("JEU MOTUS")


    dico = charger("dictionnaire.txt")
    mot = random.choice(dico).upper()
    '''mot = 'CITRON''' # si vous voulez tester avec un mot simple, mettez les deux lignes précédentes en commentaire et supprimez le commentaire de "mot = "Citron", en faisant cela et en relançant, le mot sera automatiquement CITRON et pas un mot du dico.
    tries = 0
    grid = []
    frame = tk.Frame(root)
    frame.pack(pady=20)
    init_grid()
    setup_entries()
    submit_btn = tk.Button(root, text="Soumettre", command=jouer)
    submit_btn.pack(pady=10) #.pack sert à lier le boutton à sa racine
    reset_btn = tk.Button(root, text="Réinitialiser", command=reset_game)
    reset_btn.pack(pady=10)
    boutton_abandonner = tk.Button(root, text="Abandonner", command=abandonner, bg='red', fg='white',font=("Helvetica", 11, "italic"))
    boutton_abandonner.pack(pady=16)
    root.mainloop()

def abandonner(): # cette fonction sert à arrêter le jeu grâce au .destroy qui "détruit" le prog.
    root.destroy()

def lancer_jeu(): #cette fonction sert à initialiser le djeu
    fenetre_avant_jeu.destroy() #On ferme la fenêtre
    fenetre_du_jeu() #On lance le jeu

def arreter_le_jeu(): #cette fonction sert à arrêter le jeu grâce au .destroy encore.
    fenetre_avant_jeu.destroy()  # On ferme la fenêtre


#TOUT CELA CONCERNE LA PREMIèRE FENÊTRE DU JEU!!
fenetre_avant_jeu = tk.Tk()
fenetre_avant_jeu.title("Menu de démarrage MOTUS")
fenetre_avant_jeu.geometry("2000x1332")
image = Image.open("image_intro.png", mode='r') #importation de l'image
photo = ImageTk.PhotoImage(image)
# Créer un label avec le fond
bg_label = tk.Label(fenetre_avant_jeu, image=photo)
bg_label.place(relwidth=1, relheight=1)

# Créer une frame pour contenir les bouttons
button_frame = tk.Frame(fenetre_avant_jeu, bg="white", bd=5)
button_frame.place(relx=0.5, rely=0.5, anchor='center')

# Ajouter des bouttons "Démarrer" et "Fermer"
start_button = tk.Button(button_frame, text="Démarrer le jeu", command=lancer_jeu, font=("Helvetica", 35, "italic", "bold"),fg="red")
start_button.pack(side="left", padx=0)
close_button = tk.Button(button_frame, text="Fermer", command=arreter_le_jeu, font=("Helvetica", 35, "italic", "bold"),fg="red")
close_button.pack(side="right", padx=0)

fenetre_avant_jeu.mainloop()







