from tkinter import *
from vue.screenManager import *
from vue.cadre import *
from model.game import *
from model.joueur import *

class Controller:
    """
    Classe définissant le controleur
    Possède des méthodes statiques pour les callbacks
    """

    def __init__(self, window):
        self.window = window
        self.game = Game()
        j1 = Joueur('Maitre Kacem')
        j2 = Joueur('Etudiant CM2')
        j3 = Joueur('Colson')
        self.game.addJoueur(j1)
        self.game.addJoueur(j2)
        self.game.addJoueur(j3)

        self.game.distribuerCartes()

        gameScreen = self.window.frames['GameScreen']
        gameScreen.afficherPseudoJoueurs(j1.getPseudo())
        gameScreen.afficherPseudoJoueurs(j2.getPseudo())
        gameScreen.afficherPseudoJoueurs(j3.getPseudo())
        gameScreen.cacherElementInutiles()

        print(self.game.getNBJoueurs())
        gameScreen.afficheCartes(self.game.getNBJoueurs())
