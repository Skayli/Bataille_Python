# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter import font  as tkfont # python 3
from PIL import Image,ImageTk
from vue.menuScreen import *
from vue.pseudoScreen import *
from vue.gameModeScreen import *
from vue.lobbyScreen import *
from vue.gameScreen import *

class Cadre(Tk):
    """
    Classe définissant la fenêtre principale du jeu
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.title("Jeu de la bataille")
        self.geometry("1280x720")

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuScreen, PseudoScreen, GameModeScreen, LobbyScreen, GameScreen):
            page_name = F.__name__
            frame = F(parent=self.container, mainFrame=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuScreen")

    def reset_screen(self, nom_screen):
        for key in self.frames.keys():
            if key == nom_screen:
                frame = self.frames[nom_screen]
                pageType = frame.__class__
                frame = pageType(parent=self.container, mainFrame=self)
                self.frames[nom_screen] = frame
                frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def quitter(self):
        self.destroy()
