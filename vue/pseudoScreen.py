# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class PseudoScreen(Frame):
    """
    Classe PseudoScreen permettant
    de renseigner le pseudo du Joueur
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        # Création des composants
        # Label de titre
        label = Label(self, text="Veuillez choisi un pseudo", font=mainFrame.title_font)
        # La zone de saisie pour le pseudo
        helv16 = Font(family='Helvetica', size=16, weight='bold')
        self._defaultTextEntry = True
        self._inputPseudo = Entry(self, font=helv16)
        self._inputPseudo.insert(END, "Pseudo")
        self._inputPseudo.bind("<Button-1>", self.clearDefaultTextEntry)
        # Les boutons
        self._boutonValider = Button(self, text='Continuer')
        self._boutonRetour = Button(self, text='Retour', command= lambda: self.mainFrame.show_frame("MenuScreen"))
        # Placement des composants
        label.pack(side="top", fill="x", pady=10)
        self._inputPseudo.pack(side="top", pady=10)

        self._boutonValider.pack(pady="50")
        self._boutonRetour.pack(pady="50")

        helv36 = Font(family='Helvetica', size=20, weight='bold')
        self._boutonValider.configure(font = helv36)
        self._boutonRetour.configure(font = helv36)

    def getBoutonValider(self):
        return self._boutonValider

    def getBoutonRetour(self):
        return self._boutonRetour

    def getInputPseudo(self):
        return self._inputPseudo

    def clearDefaultTextEntry(self, event):
        if (self._defaultTextEntry):
            self._inputPseudo.delete(0, END)
            self._defaultTextEntry = False
