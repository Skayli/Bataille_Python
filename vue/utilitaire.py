from tkinter import *
from PIL import Image,ImageTk

class Utilitaire:
    """
    Classe avec des fonctions utiles pour le positionnement des objets sur la fenêtre et des trucs du genre. You know it
    """
    def centrer_ligne_de_cartes(nb_cartes, largeur_element, hauteur_element, widget):
        longueur_elements = ( (nb_cartes*largeur_element) + ((nb_cartes-1)*(largeur_element/2)) )
        width_canvas = int(widget.cget('width'))
        differenceX = width_canvas - longueur_elements
        decalageX = differenceX/2
        x = decalageX - largeur_element

        hauteur_elements = hauteur_element
        height_canvas = int(widget.cget('height'))
        differenceY = height_canvas - hauteur_elements
        decalageY = differenceY/2
        y = decalageY + (hauteur_element/2)

        return (x, y)

    def centrer_ligne_de_cartes_v2(liste, widget):
        longueur_elements = ( (len(liste)*largeur_element) + ((len(liste)-1)*(largeur_element/2)) )
        width_canvas = int(widget.cget('width'))
        differenceX = width_canvas - longueur_elements
        decalageX = differenceX/2
        x = decalageX - (largeur_element/2)

        hauteur_elements = hauteur_element
        height_canvas = int(widget.cget('height'))
        differenceY = height_canvas - hauteur_elements
        decalageY = differenceY/2
        y = decalageY + (hauteur_element/2)

        return (x, y)

    def placer_en_bas_a_droite(widget, photo):
        None


    centrer_ligne_de_cartes = staticmethod(centrer_ligne_de_cartes)
