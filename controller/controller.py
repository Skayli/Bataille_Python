from tkinter import *
from vue.screenManager import *
from vue.cadre import *
from model.game import *

class Controller:
    """
    Classe définissant le controleur
    Possède des méthodes statiques pour les callbacks
    """

    def __init__(self, window):
        self.window = window
        self.game = Game()
