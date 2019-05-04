# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class MenuScreen(Frame):
    """
    Classe MenuScreen héritant de Screen
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        # Création label menu titre
        label = Label(self, text="Bienvenue dans la Bataille", font=mainFrame.title_font)
        label.pack(side="top", fill="x", pady=10)
        # Création boutons
        self._boutonCommencer = Button(self, text='Commencer', command= lambda: mainFrame.show_frame("PseudoScreen"))
        self._boutonQuitter = Button(self, text='Quitter', command= lambda: self.actionQuitter())

        self._boutonCommencer.pack(pady="50")
        self._boutonQuitter.pack(pady="50")

        helv36 = Font(family='Helvetica', size=20, weight='bold')
        self._boutonCommencer.configure(font = helv36)
        self._boutonQuitter.configure(font = helv36)

    def getBoutonCommencer(self):
        return self._boutonCommencer

    def getBoutonQuitter(self):
        return self._boutonQuitter

    def actionQuitter(self):
        self.mainFrame.quitter()
