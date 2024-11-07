import tkinter as tk

def create_sudoku_grid():

    root = tk.Tk()
    root.title("Grille Sudoku") #Inspiration du MOTUS, on initie la grille et on lui met un titre


    for i in range(9):
        for j in range(9):

            entry = tk.Entry(root, width=2, font=('Helvetica', 60, "bold"), relief = "solid", justify='center', borderwidth=7, bg = "white")
            entry.grid(row=i, column=j, padx=0, pady=0)


    root.mainloop()

create_sudoku_grid()

