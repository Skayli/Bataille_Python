# On importe Tkinter
# import tkinter as tk
from tkinter import *
from tkinter import font  as tkfont # python 3
from PIL import Image,ImageTk
from vue.menuScreen import *
from vue.pseudoScreen import *
from vue.gameModeScreen import *
from vue.hebergerScreen import *
from vue.rejoindreScreen import *
from vue.gameScreen import *
import queue as Queue

class Cadre(Tk):
    """
    Classe définissant la fenêtre principale du jeu
    """
    def __init__(self, queue, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # La Queue pour les refresh de la GUI
        self._queue = queue
        # Adapteur_vue
        self._adapteur_vue = None
        # Controller
        self._contoller = None
        # Composants graphiques
        self.title_font = tkfont.Font(family='Helvetica', size=20, weight="bold")
        self._helv20 = Font(family='Helvetica', size=20, weight='bold')

        self.title("Jeu de la bataille")
        self.geometry("1366x768")

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuScreen, PseudoScreen, GameModeScreen, HebergerScreen, RejoindreScreen, GameScreen):
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
                self.frames[nom_screen].setController(self._controller)
                frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def quitter(self):
        self.destroy()

    def setAdapteurVue(self, adapteur_vue):
        self._adapteur_vue = adapteur_vue
        adapteur_vue.setCadre(self)

    def setController(self, controller):
        self._controller = controller
        for key, frame in self.frames.items():
            frame.setController(self._controller)

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self._queue.qsize():
            try:
                msg = self._queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                if (self._adapteur_vue.isCommand(msg) == True):
                    self._adapteur_vue.analyseCommand(msg)
                print(msg)
            except Queue.Empty:
                pass
    def addQueue(self, request):
        self._queue.put(request)
