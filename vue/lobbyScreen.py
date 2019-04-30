from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class LobbyScreen(Frame):
    """
    Classe LobbyScreen qui définit le 'salon'
    de création de pseudo du Joueur
    Peut aussi servir pour patienter en attendant
    d'autres joueurs
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        # Titre du Frame
        label = Label(self, text="Lobby", font=mainFrame.title_font)
        label.pack(side="top", fill="x", pady=10)
        # La zone de saisie pour le pseudo
        helv16 = Font(family='Helvetica', size=16, weight='bold')
        self._defaultTextEntry = True
        self._inputPseudo = Entry(self, font=helv16)
        self._inputPseudo.insert(END, "Votre Pseudo")
        self._inputPseudo.bind("<Button-1>", self.clearDefaultTextEntry)
        self._inputPseudo.pack()
        # Les boutons
        self._boutonJouer = Button(self, text='Jouer', command= lambda: mainFrame.show_frame("GameScreen"))
        self._boutonRetour = Button(self, text='Quitter', command= lambda: self.actionRetour())

        self._boutonJouer.place(relx=0.25, rely=0.90, anchor=SW)
        self._boutonRetour.place(relx=0.75, rely=0.90, anchor=SE)

        helv36 = Font(family='Helvetica', size=20, weight='bold')
        self._boutonJouer.configure(font = helv36)
        self._boutonRetour.configure(font = helv36)

    def getBoutonJouer(self):
        return self._boutonJouer

    def getBoutonQuitter(self):
        return self._boutonRetour

    def clearDefaultTextEntry(self, event):
        if (self._defaultTextEntry):
            self._inputPseudo.delete(0, END)
            self._defaultTextEntry = False

    def actionRetour(self):
        self.mainFrame.show_frame("MenuScreen")
