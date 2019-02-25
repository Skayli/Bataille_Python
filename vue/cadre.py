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
        self._root = master
        self._root.geometry('{0}x{1}'.format(width, height))
        self._root.configure(bg='blue')
        # master.configure(background=str(background))
        # self.configure(background=str(background))
        Frame.__init__(self, master)
        self.configure(background=background)
        self.configure(width=800, height=800)
        # super(Cadre, self).__init__()
        # self.configure(background='blue')
        # print(self.tk.keys())ccd

        self._screenManager = ScreenManager()

    def affiche(self):
        self.grid(row=0, column=0)
        self._screenManager.getScreenCourant().affiche()
        # self.mainloop()

    def getRootPanel(self):
        return self._root

    def getScreenManager(self):
        return self._screenManager

    def modifyScreen(self, screenName):
        self._screenManager.getScreenCourant().getCanvas().place_forget()

        self._screenManager.setScreenCourant(screenName)
        # print(self._screenManager.getScreenCourant().getType())
        self._screenManager.getScreenCourant().affiche()
        # self._root.update()

    def quitter(self):
        self._root.destroy()
