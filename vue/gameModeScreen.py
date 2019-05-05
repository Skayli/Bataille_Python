# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

# class MenuScreen(Frame):
#     """
#     Classe MenuScreen héritant de Screen
#     Définit le menu principal de l'application
#     """
#
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         button1 = Button(self, text="Go to gameScreen", command=lambda: controller.show_frame("GameScreen"))
#         button1.pack()
#         # self._boutonJouer = Button(self._canvas, text='Jouer', command= lambda: self.actionJouer())
#         # self._boutonQuitter = Button(self._canvas, text='Quitter', command= lambda: self.actionQuitter())
#         #
#         # self._boutonJouer.place(relx=0.25, rely=0.90, anchor=SW)
#         # self._boutonQuitter.place(relx=0.75, rely=0.90, anchor=SE)
#         #
#         # helv36 = Font(family='Helvetica', size=20, weight='bold')
#         # self._boutonJouer.configure(font = helv36)
#         # self._boutonQuitter.configure(font = helv36)
#
#     def getBoutonJouer(self):
#         return self._boutonJouer
#
#     def getBoutonQuitter(self):
#         return self._boutonQuitter
#
#     def actionJouer(self):
#         self._parent.modifyScreen('GameScreen')
#
#     def actionQuitter(self):
#         self._parent.quitter()

class GameModeScreen(Frame):
    """
    Classe GameModeScreen héritant de Screen
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        label = Label(self, text="Sélection du mode de jeu", font=mainFrame.title_font)
        label.pack(side="top", fill="x", pady=10)

        self._boutonHeberger = Button(self, text='Héberger une partie')
        self._boutonRejoindre = Button(self, text='Rejoindre une partie')
        self._boutonQuitter = Button(self, text='Quitter', command= lambda: self.mainFrame.quitter())

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

    def getBoutonHeberger(self):
        return self._boutonHeberger

    def getBoutonRejoindre(self):
        return self._boutonRejoindre

    def getBoutonQuitter(self):
        return self._boutonQuitter
