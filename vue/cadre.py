# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter import font  as tkfont # python 3
from PIL import Image,ImageTk
from vue.menuScreen import MenuScreen
from vue.gameScreen import GameScreen
from vue.lobbyScreen import LobbyScreen

class Cadre(Tk):
    """
    Classe définissant la fenêtre principale du jeu
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.title("Jeu de la bataille")
        self.geometry("800x600")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuScreen, GameScreen, LobbyScreen):
            page_name = F.__name__
            frame = F(parent=container, mainFrame=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuScreen")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def quitter(self):
        self.destroy()
