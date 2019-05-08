# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.screen import *
from controller.controller import *

class VictoireScreen(Frame):

    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        self.config(bg='linen')
        # Création label menu titre
        self.labelTitre = Label(self, text="Résultats de la Bataille", borderwidth=2, relief="groove", font=mainFrame.title_font, bg='linen')
        self.labelTitre.pack(side="top", fill="x", pady=10, ipady=20)

        self.helv = Font(family='Helvetica', size=20, weight='bold')
        self.labelsVictoire = []

    def setTextVictoire(self, infos):
        for info in infos:
            self.labelsVictoire.append(Label(self, text=info.getVictoireInfos(), font=self.helv, bg='linen'))
        for label in self.labelsVictoire:
            label.pack(side="top", fill="x", pady=10, ipady=20)

    def setController(self, controller):
        self._controller = controller
