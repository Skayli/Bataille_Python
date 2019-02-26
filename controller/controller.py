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
<<<<<<< HEAD

     
=======
        j1 = Joueur('Maitre Kacem')
        j2 = Joueur('Etudiant CM2')
        j3 = Joueur('Colson')
        self.game.addJoueur(j1)
        self.game.addJoueur(j2)
        self.game.addJoueur(j3)

        self.game.distribuerCartes()

        self.window.frames['GameScreen'].afficherPseudoJoueurs(j1.getPseudo())
        self.window.frames['GameScreen'].afficherPseudoJoueurs(j2.getPseudo())
        self.window.frames['GameScreen'].afficherPseudoJoueurs(j3.getPseudo())
        self.window.frames['GameScreen'].cacherElementInutiles()
>>>>>>> ceb53396752fbc7b09f88f8dd1cca9435ad05aab
