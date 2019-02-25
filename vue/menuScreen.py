# On importe Tkinter
# import tkinter as tk
from tkinter import *
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
        self._boutonJouer = Button(self._canvas, text='Jouer')
        self._boutonQuitter = Button(self._canvas, text='Quitter')

        self._boutonJouer.place(relx=0.25, rely=0.80)
        self._boutonQuitter.place(relx=0.75, rely=0.80)

    def getBoutonJouer(self):
        return self._boutonJouer

    def getBoutonQuitter(self):
        return self._boutonQuitter
