# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from vue.screenManager import *

class Cadre(Frame):
    """
    Classe définissant la fenêtre principale du jeu
    """
    def __init__(self, master=None, width=800, height=600, background='magenta'):
        master.geometry('{0}x{1}'.format(width, height))
        # master.configure(background=str(background))
        # self.configure(background=str(background))
        Frame.__init__(self, master)
        self.configure(background=background)
        self.configure(width=800, height=800)
        # super(Cadre, self).__init__()
        # self.configure(background='blue')
        # print(self.tk.keys())

        self._screenManager = ScreenManager()

    def affiche(self):
        self.grid(row=0, column=0)
        self._screenManager.getScreenCourant().affiche()
        self.mainloop()

    def getRootPanel(self):
        return self._root

    def getScreenManager(self):
        return self._screenManager
