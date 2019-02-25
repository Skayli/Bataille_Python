# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
import os

class GameScreen(Screen):
    """
    Classe GameScreen héritant de Screen
    Définit le tapis de jeu composé des cartes jouées
    """

    def __init__(self, root, width=600, height=600, bg='green'):
        Screen.__init__(self, root, width, height, bg)
        self._liste_cartes_en_jeu = ["as_coeur", "as_pique", "as_trefle", "as_carreau"]
        self._dict_images = {}
        self.update_dictionnaire_images()

    def update_dictionnaire_images(self):
        # On vide le dictionnaire
        self._dict_images.clear()

        if len(self._liste_cartes_en_jeu) > 0:
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            rel_path = "../images/{0}.png"
            abs_file_path = os.path.join(script_dir, rel_path)
            photo = ImageTk.PhotoImage(file= abs_file_path.format(self._liste_cartes_en_jeu[0]))
            width = photo.width()
            height = photo.height()

            x, y = Utilitaire.centrer_ligne_de_cartes(len(self._liste_cartes_en_jeu), width, height, self.getCanvas())

            x = x + width + (width/2)
            print(x, ' ', y)
            print('CANVAS DIMENSION ', self._canvas.cget('width'), self._canvas.cget('height'))
            item = self._canvas.create_image(x,y,image=photo)
            self._dict_images[self._liste_cartes_en_jeu[0]]= photo

            for image in self._liste_cartes_en_jeu[1:]:
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                rel_path = "../images/{0}.png"
                abs_file_path = os.path.join(script_dir, rel_path)
                photo = ImageTk.PhotoImage(file= abs_file_path.format(image))

                width = photo.width()
                height = photo.height()
                x = x + width + (width/2)

                item = self._canvas.create_image(x,y,image=photo)

                self._dict_images[image]= photo

    # def update_dictionnaire_images_v2(self):
    #     # On vide le dictionnaire
    #     self._dict_images.clear()
    #
    #     if len(self._liste_cartes_en_jeu) > 0:
    #         x = 138
    #         y = 300
    #         for image in self._liste_cartes_en_jeu:
    #             photo = ImageTk.PhotoImage(file= "D:\Atom_workspace\Python\Puissance_4\images\{0}.png".format(image))
    #
    #             width = photo.width()
    #             height = photo.height()
    #             x = x + width + (width/2)
    #
    #             print(x, ' ', y)
    #
    #             item = self._canvas.create_image(x,y,image=photo)
    #
    #             self._dict_images[image]= photo
    #         print(self._dict_images)
