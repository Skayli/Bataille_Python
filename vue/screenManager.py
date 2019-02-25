# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk

class ScreenManager:
    """
    Classe permettant de gérer les différents écrans de l'application
    """

    def __init__(self):
        self._liste_screens = {}
        self._screen_courant = None
        self._screen_courant = None

    def ajouterScreen(self, key, screen):
        self._liste_screens[key] = screen

    def getScreen(self, key):
        if key in self._liste_screens:
            return self._liste_screens[key]
        return False

    def getListeScreens(self):
        return self._liste_screens

    def getScreenCourant(self):
        return self._screen_courant

    def setScreenCourant(self, key):
        self._screen_courant = self.getScreen(key)

    def printKeysScreenList(self):
        for key, value in self._liste_screens.items():
            print('{0}\n'.format(key))

    def actionJouer():
        print('Jouer')
        gameScreen = self.getScreen('GameScreen')
        if gameScreen != False:
            self._cadre.setScreenCourant(gameScreen)

    def actionQuitter():
        print('Quitter')
