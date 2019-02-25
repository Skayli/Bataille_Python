"""Premier exemple avec Tkinter.

On crée une fenêtre simple qui souhaite la bienvenue à l'utilisateur.

"""

# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk

# On crée une fenêtre, racine de notre interface
root = Tk()
root.geometry("800x600")
root.configure(background='blue')

# On crée un label (ligne de texte) souhaitsant la bienvenue
# Note : le premier paramètre passé au constructeur de Label est notre
# interface racine
champ_label = Label(root, text="La bataille de Colson")
image_loic_possede = ImageTk.PhotoImage(Image.open("D:\Atom_workspace\Python\Puissance_4\loic_possede.jpg"))
image = Image.open("D:\Atom_workspace\Python\Puissance_4\loic_possede.jpg")

image_loic_endormi = ImageTk.PhotoImage(Image.open("D:\Atom_workspace\Python\Puissance_4\loic_endormi.jpg"))

panel_gauche = Label(root, image = image_loic_possede)
panel_droit = Label(root, image = image_loic_endormi)

canvas = Canvas(root, width=image.size[0], height = image.size[1])
canvas.create_image(0,0, anchor = NW, image=image_loic_possede)
canvas.pack()

panel_gauche.configure(background='green')
panel_droit.configure(background='red')

panel_gauche.configure()

# On affiche le label dans la fenêtre
champ_label.pack()

# panel_gauche.pack(side = "left", fill = "both", expand = "yes")
# panel_droit.pack(side = "right", fill = "both", expand = "yes")

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
root.mainloop()
