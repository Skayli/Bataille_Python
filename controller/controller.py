from tkinter import *
from vue.screenManager import *
from vue.cadre import *
from model.game import *

class Controller:
    """
    Classe définissant le controleur
    Possède des méthodes statiques pour les callbacks
    """

    def __init__(self, cadre, game):
        self._cadre = cadre
        self._game = game

    def getGame(self):
        return self._game

    def getCadre(self):
        return self._cadre
