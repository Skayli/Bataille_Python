# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from utilitaire import *

def callback(event):
    print('Clic sur pile joueur !', event.x, event.y)

def changeMousePointerToHand(event, widget):
        widget.configure(cursor="hand2")

def changeMousePointerToBasic(event, widget):
        widget.configure(cursor="")

# On crée une fenêtre, racine de notre interface
root = Tk()
root.geometry("800x600")
root.configure(background='magenta')

# On crée un label (ligne de texte) souhaitsant la bienvenue
# Note : le premier paramètre passé au constructeur de Label est notre
# interface racine
champ_label = Label(root, text="La bataille de Colson")

liste_cartes_jouees = ["as_coeur", "as_pique", "as_trefle"]
pile_joueur = 'face_cachee.png'

pile_joueur_image_tk = ImageTk.PhotoImage(file= "D:\Atom_workspace\Python\Puissance_4\images\{}".format(pile_joueur))

gifsdict={}

# creation d'un widget 'canvas' contenant des images bitmap:

canvas_tapis=Canvas(root, width =600, height = 600, bg ='green')

x, y = Utilitaire.centrer_ligne_de_cartes(liste_cartes_jouees, 72, 96, canvas_tapis)

# print(type(x) , " valeur x = {}".format(x))

for image in liste_cartes_jouees:

    # picture = Image.open("D:\Atom_workspace\Python\Puissance_4\images\{}".format(image))
    photo = ImageTk.PhotoImage(file= "D:\Atom_workspace\Python\Puissance_4\images\{}.png".format(image))

    # width, height = picture.size
    # print('Dimensions picture = ', width, ' ', height)
    # x, y = Utilitaire.centrer_ligne_de_cartes(liste_cartes_jouees, 72, 96, canvas_tapis)

    # print(picture)
    print('Dimensions de PhotoImage = ', photo.width(), ' ', photo.height())

    width = photo.width()
    height = photo.height()
    x = x + width + (width/2)

    item = canvas_tapis.create_image(x,y,image=photo)

    gifsdict[image]= photo
    # mise en page à l'aide de la méthode 'grid':
    # canvas_tapis.grid()

print(gifsdict)

id_pile_joueur = canvas_tapis.create_image(600-71-10,600-96-10,image=pile_joueur_image_tk)
print(id_pile_joueur)
canvas_tapis.tag_bind(id_pile_joueur, '<ButtonRelease-1>', callback)
canvas_tapis.tag_bind(id_pile_joueur, '<Enter>', lambda event : changeMousePointerToHand(event, canvas_tapis))
canvas_tapis.tag_bind(id_pile_joueur, '<Leave>', lambda event : changeMousePointerToBasic(event, canvas_tapis))

canvas_tapis.pack()
# On affiche le label dans la fenêtre
champ_label.pack()

# panel_gauche.pack(side = "left", fill = "both", expand = "yes")
# panel_droit.pack(side = "right", fill = "both", expand = "yes")

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
root.mainloop()
