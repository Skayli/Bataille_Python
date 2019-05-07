# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class GameModeScreen(Frame):
    """
    Classe GameModeScreen héritant de Screen
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        self.config(bg='linen')
        self._label_bienvenue = Label(self, text='', bg='linen', borderwidth=2, relief="groove", font=mainFrame.title_font)
        self._label_bienvenue.pack(side="top", fill="x", pady=10, ipady=20)

        label = Label(self, text="Sélection du mode de jeu", bg='linen', font=mainFrame.title_font)
        label.pack(side="top", fill="x", pady=10)

        self._boutonHeberger = Button(self, text='Héberger une partie', bg='lightcyan2')
        self._boutonRejoindre = Button(self, text='Rejoindre une partie', bg='lightcyan2')
        self._boutonQuitter = Button(self, text='Quitter', bg='lightcyan2', command= lambda: self.mainFrame.quitter())

        # self._boutonHeberger.place(relx=0.25, rely=0.5, anchor=S)
        # self._boutonRejoindre.place(relx=0.5, rely=0.5, anchor=S)
        # self._boutonQuitter.place(relx=0.75, rely=0.90, anchor=S)
        self._boutonHeberger.pack(pady="50")
        self._boutonRejoindre.pack(pady="50")
        self._boutonQuitter.pack(pady="50")

        helv36 = Font(family='Helvetica', size=20, weight='bold')
        self._boutonHeberger.configure(font = helv36)
        self._boutonRejoindre.configure(font = helv36)
        self._boutonQuitter.configure(font = helv36)

    def setController(self, controller):
        self._controller = controller

    def getBoutonHeberger(self):
        return self._boutonHeberger

    def getBoutonRejoindre(self):
        return self._boutonRejoindre

    def getBoutonQuitter(self):
        return self._boutonQuitter
