# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class MenuScreen(Screen):
    """
    Classe MenuScreen héritant de Screen
    Définit le menu principal de l'application
    """

    def __init__(self, root, width=600, height=600, bg='white'):
        Screen.__init__(self, root, width, height, bg)
        self._boutonJouer = Button(self._canvas, text='Jouer', command= lambda: self.actionJouer())
        self._boutonQuitter = Button(self._canvas, text='Quitter', command= lambda: self.actionQuitter())

        self._boutonJouer.place(relx=0.25, rely=0.90, anchor=SW)
        self._boutonQuitter.place(relx=0.75, rely=0.90, anchor=SE)

        helv36 = Font(family='Helvetica', size=20, weight='bold')
        self._boutonJouer.configure(font = helv36)
        self._boutonQuitter.configure(font = helv36)

    def getBoutonJouer(self):
        return self._boutonJouer

    def getBoutonQuitter(self):
        return self._boutonQuitter

    def actionJouer(self):
        self._parent.modifyScreen('GameScreen')

    def actionQuitter(self):
        self._parent.quitter()
