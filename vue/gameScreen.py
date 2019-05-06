# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from tkinter.font import Font
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
        # Infos sur les éléments constituant le plateau
        self._nomJoueurPrincipal = None
        self._joueurs = []
        self._piles_FC = {}
        self._dict_imagesCartes = {}
        self._cartePile = None
        self._carteAJouer = None
        self._index_cartes_sur_tapis = 0
        self._peutJouer = False
        # Label titre
        label = Label(self, text="Jeu de la bataille", font=mainFrame.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid(row=0, column=1)

        self._canvas = Canvas(self, width=800, height=600, bg='green')
        # Gestion évènements
        self._canvas.bind('<B1-Motion>', self.moveCard)
        # Dessin du cadre dans lequel faudra placer les cartes
        self._tag_zone_jeu = 'zone_jeu'
        self._x1, self._y1, self._x2, self._y2 = 150, 150, (int(self._canvas.cget('width'))-150), (int(self._canvas.cget('height'))-150)
        self._zoneJeu = self._canvas.create_rectangle(self._x1, self._y1, self._x2, self._y2, width='2', tags=self._tag_zone_jeu)
        # print('zone de jeu = %d' % self._zoneJeu)
        # self._canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        # self._canvas.pack(side="bottom", fill="both")
        self._canvas.grid(row=2, column=1)

        # self._liste_cartes_en_jeu = ["as_coeur", "as_pique", "as_trefle", "as_carreau"]
        # self._liste_cartes_en_jeu = ["face_cachee"]
        # self.update_dictionnaire_images()

        helv12 = Font(family='Helvetica', size=12, weight='bold')
        # self.labelsJoueurs = [Label(self._canvas, text=''), Label(self._canvas, text=''), Label(self._canvas, text=''), Label(self._canvas, text='')]
        # self.labelsJoueurs = [Label(self, text=''), Label(self, text=''), Label(self, text=''), Label(self, text='')]
        self.labelsJoueurs = []
        for i in range(4):
            self.labelsJoueurs.append(Label(self, text='', font=helv12))

        # self.labelsJoueurs[0].place(relx=0.5, rely=0.98, anchor=S)
        # self.labelsJoueurs[1].place(relx=0.5, rely=0.02, anchor=N)
        # self.labelsJoueurs[2].place(relx=0.95, rely=0.5, anchor=E)
        # self.labelsJoueurs[3].place(relx=0.05, rely=0.5, anchor=W)
        # self.placerLabelsJoueurs()
        # Config en plus
        # self.labelsJoueurs[0].configure(borderwidth=4, relief='solid')
        boutonRetour = Button(self, text="Retour au menu", command=lambda: mainFrame.show_frame("LobbyScreen"))
        # button1.pack()
        boutonRetour.grid(row=4, column=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2, minsize=600)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

    def setController(self, controller):
        self._controller = controller

    def placerLabelsJoueurs(self):
        indexJouerPrincipal = self.trouverIndexJoueurPrincipal()
        haut, gauche, droite = False, False, False
        self.labelsJoueurs[indexJouerPrincipal].grid(row=3, column=1, ipadx=10, ipady=10)
        for i in range(len(self.labelsJoueurs)):
            if i != indexJouerPrincipal:
                if haut == False:
                    self.labelsJoueurs[i].grid(row=1, column=1, ipadx=10, ipady=10)
                    haut = True
                elif gauche == False:
                    self.labelsJoueurs[i].grid(row=2, column=0, ipadx=10, ipady=10)
                    gauche = True
                elif droite == False:
                    self.labelsJoueurs[i].grid(row=2, column=2, ipadx=10, ipady=10)
                    droite = True

    def update_dictionnaire_images(self):
        # On vide le dictionnaire
        self._dict_imagesCartes.clear()

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
            self._dict_imagesCartes[self._liste_cartes_en_jeu[0]]= photo
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
                self._dict_imagesCartes[image]= photo
                self._canvas.tag_bind(item, '<Button-1>', self.selectionnerCarte)

    def afficheCartes(self, nbJoueurs):
        for i in range(0, (nbJoueurs-1)):
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            rel_path = "../images/face_cachee.png"
            abs_file_path = os.path.join(script_dir, rel_path)

            photo = ImageTk.PhotoImage(file= abs_file_path)
            widthCanvas = int(self._canvas.cget('width'))
            heightCanvas = int(self._canvas.cget('height'))
            widthCarte = photo.width()
            heightCarte = photo.height()
            x = widthCanvas/2
            y = heightCanvas - (heightCarte/2)
            tag = ('carte_%d' % i)
            item = self._canvas.create_image(x, y, image=photo, tags=tag)
            # print(item)
            self._dict_imagesCartes[i]= photo
            self._canvas.tag_bind(item, '<Button-1>', self.selectionnerCarte)

    def updateLayout(self):
        self.placerLabelsJoueurs()
        self.afficherCartesPiles()
        self.afficherCarteAJouer()

    def afficherCarteAJouer(self):
        # self._dict_imagesCartes.clear()
        # On cherche l'image de la carte
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "../images/face_cachee.png"
        abs_file_path = os.path.join(script_dir, rel_path)
        photo = ImageTk.PhotoImage(file= abs_file_path)
        widthCanvas = int(self._canvas.cget('width'))
        heightCanvas = int(self._canvas.cget('height'))
        widthCarte = photo.width()
        heightCarte = photo.height()
        self._x_BaseCarteAJouer = widthCanvas/2
        self._y_BaseCarteAJouer = heightCanvas - (heightCarte/2)
        tag = 'carte_a_jouer'
        self._cartePile = self._canvas.create_image(self._x_BaseCarteAJouer, self._y_BaseCarteAJouer, image=photo, tags=tag)
        self._dict_imagesCartes[self._index_cartes_sur_tapis]= photo
        # self._index_cartes_sur_tapis += 1
        self._canvas.tag_bind(self._cartePile, '<Button-1>', self._controller.selectionnerCarte)
        # self._canvas.tag_bind(self._cartePile, '<Button-1>', self.selectionnerCarte)

    def afficherCartesPiles(self):
        # On vide le dictionnaire
        # self._dict_imagesCartes.clear()
        bas, haut, gauche, droite = False, False, False, False
        # On cherche l'image de la carte
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "../images/face_cachee.png"
        abs_file_path = os.path.join(script_dir, rel_path)

        widthCanvas = int(self._canvas.cget('width'))
        heightCanvas = int(self._canvas.cget('height'))
        witdhCarte, heightCarte = 0, 0
        x_baseCarte, y_baseCarte = 0, 0

        for i in range(self.getNombreJoueurs()):
            photo = ImageTk.PhotoImage(file= abs_file_path)
            if bas == False:
                widthCarte = photo.width()
                heightCarte = photo.height()
                x_baseCarte = widthCanvas/2
                y_baseCarte = heightCanvas - (heightCarte/2)
                tag = 'carte_pile_bas'
                item = self._canvas.create_image(x_baseCarte, y_baseCarte, image=photo, tags=tag)
                self._piles_FC[tag]=photo
                bas = True
            elif haut == False:
                widthCarte = photo.width()
                heightCarte = photo.height()
                x_baseCarte = widthCanvas/2
                y_baseCarte = heightCarte/2
                tag = 'carte_pile_haut'
                item = self._canvas.create_image(x_baseCarte, y_baseCarte, image=photo, tags=tag)
                self._piles_FC[tag]=photo
                haut = True
            elif gauche == False:
                widthCarte = photo.width()
                heightCarte = photo.height()
                x_baseCarte = widthCarte/2
                y_baseCarte = heightCanvas/2
                tag = 'carte_pile_gauche'
                item = self._canvas.create_image(x_baseCarte, y_baseCarte, image=photo, tags=tag)
                self._piles_FC[tag]=photo
                gauche = True
            elif droite == False:
                widthCarte = photo.width()
                heightCarte = photo.height()
                x_baseCarte = widthCanvas - (widthCarte/2)
                y_baseCarte = heightCanvas/2
                tag = 'carte_pile_droite'
                item = self._canvas.create_image(x_baseCarte, y_baseCarte, image=photo, tags=tag)
                self._piles_FC[tag]=photo
                droite = True
        # widthCanvas = int(self._canvas.cget('width'))
        # heightCanvas = int(self._canvas.cget('height'))
        # widthCarte = photo.width()
        # heightCarte = photo.height()
        # self._x_BaseCarteAJouer = widthCanvas/2
        # self._y_BaseCarteAJouer = heightCanvas - (heightCarte/2)
        # tag = 'carte_a_jouer'
        # item = self._canvas.create_image(self._x_BaseCarteAJouer, self._y_BaseCarteAJouer, image=photo, tags=tag)
        # self._dict_imagesCartes[self._index_cartes_sur_tapis]= photo
        # self._index_cartes_sur_tapis += 1
        # self._canvas.tag_bind(item, '<Button-1>', self.selectionnerCarte)

    def placerCarteJouee(self, nomFichierCarte, nomCarte):
        photo = ImageTk.PhotoImage(file= nomFichierCarte)
        coordsCarte = self._canvas.coords(self._cartePile)
        x, y = coordsCarte[0], coordsCarte[1]
        tag = nomCarte
        item = self._canvas.create_image(x, y, image=photo, tags=tag)
        # self._dict_imagesCartes[self._index_cartes_sur_tapis]= photo
        self._dict_imagesCartes[tag]= photo
        self._index_cartes_sur_tapis += 1

    def resetPositionCartePile(self):
        self._canvas.coords(self._cartePile, self._x_BaseCarteAJouer, self._y_BaseCarteAJouer)
        self._canvas.tag_raise(self._cartePile)

    def selectionnerCarte(self, event):
        if (self._peutJouer == True):
            print('entre dans selection carte')
            # self._cartePile = self._canvas.find_closest(event.x, event.y)[0] # Le 0 c'est car on prend la 1ere
            self._carteAJouer = self._canvas.find_withtag('carte_a_jouer')[0]

    def moveCard(self, event):
        if self._carteAJouer is not None:
            print('move carte')
            self._canvas.coords(self._cartePile, event.x, event.y)

    def relacherCarte(self, event):
        if self._cartePile is not None:
            print('carte relachee')
            enclosedObjects = self._canvas.find_enclosed(self._x1, self._y1, self._x2, self._y2)
            print(enclosedObjects)
            if len(enclosedObjects) > 0:
                for item in enclosedObjects:
                    if (item is self._cartePile):
                        None
            self._cartePile = None

    def showCarte(self, nomFichierCarte, nomCarte, x, y):
        photo = ImageTk.PhotoImage(file= nomFichierCarte)
        tag = nomCarte
        item = self._canvas.create_image(x, y, image=photo, tags=tag)
        # self._dict_imagesCartes[self._index_cartes_sur_tapis]= photo
        self._dict_imagesCartes[tag]= photo
        self._index_cartes_sur_tapis += 1

    def getEnclosedObjectsZoneJeu(self):
        return self._canvas.find_enclosed(self._x1, self._y1, self._x2, self._y2)

    def getCanvas(self):
        return self._canvas

    def getCartePile(self):
        return self._cartePile

    def setCartePile(self, value):
        self._cartePile = value

    def getIndexCartesSurTapis(self):
        return self._index_cartes_sur_tapis

    def get_zoneJeu_X1():
        return self._x1

    def get_zoneJeu_Y1():
        return self._y1

    def get_zoneJeu_X2():
        return self._x2

    def get_zoneJeu_Y2():
        return self._y2

    def getNomJoueurPrincipal(self):
        return self._nomJoueurPrincipal

    def setNomJoueurPrincipal(self, nom):
        self._nomJoueurPrincipal = nom

    def getNombreJoueurs(self):
        return len(self._joueurs)

    def peutJouer(self):
        return self._peutJouer

    def setPeutJouer(self, value):
        self._peutJouer = value

    def ajouterInfosJoueur(self, infos, nom):
        for label in self.labelsJoueurs:
            if label['text'] == '':
                label['text'] = str(infos)
                self._joueurs.append(nom)
                break

    def modifierInfosJoueurAt(self, infos, nom, index):
        if index < len(self.labelsJoueurs):
            self.labelsJoueurs[index]['text'] = infos

    def trouverIndexJoueurPrincipal(self):
        for i in range(len(self._joueurs)):
            if (self._joueurs[i] == self._nomJoueurPrincipal):
                return i
        return None

    def cacherElementInutiles(self):
        for label in self.labelsJoueurs:
            if label['text'] == '':
                label.place_forget()
