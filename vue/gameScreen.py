# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
import os

class GameScreen(Frame):
    """
    Classe GameScreen héritant de Screen
    Définit le tapis de jeu composé des cartes jouées
    """

    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        label = Label(self, text="Page du game", font=mainFrame.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Voir la page menuScreen", command=lambda: mainFrame.show_frame("MenuScreen"))
        button1.pack()

        self._canvas = Canvas(self, width=600, height=600, bg='green')
        self._canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        self._liste_cartes_en_jeu = ["as_coeur", "as_pique", "as_trefle", "as_carreau"]
        self._dict_images = {}

        self.update_dictionnaire_images()

        self.labels = [Label(self._canvas, text=''), Label(self._canvas, text=''), Label(self._canvas, text=''), Label(self._canvas, text='')]

        self.labels[0].place(relx=0.5, rely=0.98, anchor=S)
        self.labels[1].place(relx=0.5, rely=0.02, anchor=N)
        self.labels[2].place(relx=0.95, rely=0.5, anchor=E)
        self.labels[3].place(relx=0.05, rely=0.5, anchor=W)

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
            self._canvas.tag_bind(item, '<Button-1>', self.selectionnerCarte)
            self._canvas.bind('<B1-Motion>', self.moveCard)
            self._canvas.bind('<ButtonRelease-1>', self.relacherCarte)

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
                self._canvas.tag_bind(item, '<Button-1>', self.selectionnerCarte)

    def selectionnerCarte(self, event):
        print('entre dans selection carte')
        self.carte = self._canvas.find_closest(event.x, event.y)

    def moveCard(self, event):
        print('move carte')
        if self.carte is not None:
            self._canvas.coords(self.carte, event.x, event.y)

    def relacherCarte(self, event):
        print('carte relachee')
        self.carte = None

    def getCanvas(self):
        return self._canvas

    def afficherPseudoJoueurs(self, pseudo):
        for label in self.labels:
            if label['text'] == '':
                label['text'] = str(pseudo)
                break

    def cacherElementInutiles(self):
        for label in self.labels:
            if label['text'] == '':
                label.place_forget()
