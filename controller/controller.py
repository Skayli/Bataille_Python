from tkinter import *
from vue.screenManager import *
from vue.cadre import *
from model.game import *
from model.joueur import *
import os

class Controller:
    """
    Classe définissant le controleur
    Possède des méthodes statiques pour les callbacks
    """

    def __init__(self, window):
        self._window = window
        self._game = None
        self._mainPlayer = None
        self._othersPlayers = []
        # j1 = Joueur('Maitre Kacem')
        # j2 = Joueur('Etudiant CM2')
        # j3 = Joueur('Bouteille d\'eau')
        # j4 = Joueur('Le testeur de jeu')
        # self._game.addJoueur(j1)
        # self._game.addJoueur(j2)
        # self._game.addJoueur(j3)
        # self._game.addJoueur(j4)
        #
        # self._game.distribuerCartes()
        #
        self.initGameScreen()
        # self._gameScreen.afficherPseudoJoueurs(j1.getPseudo())
        # self._gameScreen.afficherPseudoJoueurs(j2.getPseudo())
        # self._gameScreen.afficherPseudoJoueurs(j3.getPseudo())
        # self._gameScreen.afficherPseudoJoueurs(j4.getPseudo())
        # self._gameScreen.cacherElementInutiles()

        # print('Nombre de Joueurs au début %d' % self._game.getNBJoueurs())
        # self._gameScreen.afficheCartes(self._game.getNBJoueurs())

        self._lobbyScreen = self._window.frames['LobbyScreen']
        # self._lobbyScreen._boutonValiderPseudo.config(command=self.validerPseudo)
        self._lobbyScreen._boutonJouer.config(command=self.validerPartieSolo)

    def initGameScreen(self):
        self._gameScreen = self._window.frames['GameScreen']
        # Gestion des évènements sur le canvas
        self._gameScreen.getCanvas().bind('<B1-Motion>', self.moveCard)
        self._gameScreen.getCanvas().bind('<ButtonRelease-1>', self.relacherCarte)

    def validerPseudo(self):
        pseudo = self._lobbyScreen._inputPseudo.get()
        print('Pseudo du joueur principal %s' % pseudo)
        self._mainPlayer = Joueur(pseudo)
        self._game.addJoueur(self._mainPlayer)
        print('Nombre de Joueurs après création joueur principal %d' % self._game.getNBJoueurs())

    def validerPartieSolo(self):
        # On reset la partie pour etre safe
        self._game = Game()
        self._window.reset_screen("GameScreen")
        self.initGameScreen()
        # Gestion du joueur principal
        pseudo = self._lobbyScreen._inputPseudo.get()
        print('Pseudo du joueur principal %s' % pseudo)
        self._mainPlayer = Joueur(pseudo)
        self._game.addJoueur(self._mainPlayer)
        self._gameScreen.afficherPseudoJoueurs(self._game.getJoueur(0).getPseudo())
        # Gestion des adversaires
        nombreAdversaires = int(self._lobbyScreen.getSelectedItemComboBoxAdversaires()[0])
        print('Nombre d\'adversaires choisi %s' % nombreAdversaires)
        for i in range(0,nombreAdversaires):
            self._othersPlayers.append(Joueur(('Adversaire %d' % (i+1))))
            self._game.addJoueur(self._othersPlayers[i])
            self._gameScreen.afficherPseudoJoueurs((self._game.getJoueur(i+1).getPseudo()))
        # On prépare la partie
        self._game.distribuerCartes()
        self._gameScreen.cacherElementInutiles()
        self._gameScreen.afficherCarteFC()
        # self._gameScreen.afficheCartes(self._game.getNBJoueurs())
        # On change d'écran
        self._window.show_frame("GameScreen")

    def moveCard(self, event):
        if self._gameScreen.getCarteFC() is not None:
            print('move carte')
            self._gameScreen.getCanvas().coords(self._gameScreen.getCarteFC(), event.x, event.y)

    def relacherCarte(self, event):
        if self._gameScreen.getCarteFC() is not None:
            print('carte relachee')
            enclosedObjects = self._gameScreen.getEnclosedObjectsZoneJeu()
            # print(enclosedObjects)
            isCarteDansZoneJeu = False
            if len(enclosedObjects) > 0:
                for item in enclosedObjects:
                    if (item is self._gameScreen.getCarteFC()):
                        isCarteDansZoneJeu = True
                        # Alors on montre la carte dans la zone de jeu
                        carteAJouer = self._mainPlayer.getCarteAJouer()
                        fileNameCarteAJouer = carteAJouer.getNomCarteFormatFichier()
                        script_dir = os.path.dirname(__file__)
                        rel_path = "..\\images\\{0}.png"
                        abs_file_path = os.path.join(script_dir, rel_path)
                        abs_file_path = abs_file_path.format(fileNameCarteAJouer)
                        print(abs_file_path)
                        # On remet la carte face cachée à sa place d'origine et affiche la carte jouée
                        self._gameScreen.placerCarteJouee(abs_file_path)
            if (isCarteDansZoneJeu == False):
                self._gameScreen.resetPositionCarteFC()
            self._gameScreen.setCarteFC(None)
