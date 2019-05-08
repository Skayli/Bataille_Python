from tkinter import *
from tkinter import messagebox
from vue.screenManager import *
from vue.cadre import *
from model.game import *
from model.joueur import *
from model.adapteur_model import *
from controller.ivyBus import *
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
        self._nbCartesJouees = 0
        self._pseudo = None
        self._statePremierCoupBataille = False
        self._ivyBus = None
        self._actionsBots = []

        # Gestion pour le GameScreen
        self.initGameScreen()
        # Gestion pour l'écran de saisie du pseudo
        self._window.frames['PseudoScreen'].getBoutonValider().config(command=self.validerPseudo)
        # Gestion écran HebergerScreen
        self._hebergerScreen = self._window.frames['HebergerScreen']
        self._hebergerScreen._boutonJouer.config(command=self.validerPartie)
        self._hebergerScreen._boutonRetour.config(command=self.quitterLobby)
        # Gestion écran RejoindreScreen
        self._rejoindreScreen = self._window.frames['RejoindreScreen']
        self._rejoindreScreen.getInputAdresse().bind('<Return>', self.validerAdresseJoindreHost)
        self._rejoindreScreen.getBoutonPret().config(command=self.validerJoueurPret)
        self._rejoindreScreen._boutonRetour.config(command=self.quitterLobby)
        # Gestion écran GameModeScreen
        self._gameModeScreen = self._window.frames['GameModeScreen']
        self._gameModeScreen.getBoutonHeberger().config(command=self.validerHeberger)
        self._gameModeScreen.getBoutonRejoindre().config(command=self.validerRejoindre)

    # Initialisation de l'écran de jeu
    def initGameScreen(self):
        self._gameScreen = self._window.frames['GameScreen']
        self._gameScreen.setNomJoueurPrincipal(self._pseudo)
        # Gestion des évènements sur le canvas
        # self._gameScreen.getCanvas().bind('<B1-Motion>', self.moveCard)
        self._gameScreen.getCanvas().bind('<ButtonRelease-1>', self.relacherCarte)

    # Validation du pseudo entré par l'utilisateur au début
    def validerPseudo(self):
        self._pseudo = self._window.frames['PseudoScreen'].getInputPseudo().get()
        print('Pseudo du joueur principal %s' % self._pseudo)
        if ("|" in self._pseudo) or ("," in self._pseudo):
            messagebox.showerror('Erreur', 'Pseudo Non Valide')
        else:
            self._gameScreen.setNomJoueurPrincipal(self._pseudo)
            # On a le nom du joueur alors on peut créer le Game
            self._game = Game(self._pseudo, self)
            # On change d'écran
            self._window.frames['GameModeScreen']._label_bienvenue['text'] = "Bienvenue {0}".format(self._pseudo)
            self._window.show_frame('GameModeScreen')

    # Validation du choix de mode de jeu où l'on souhaite HOST une partie
    def validerHeberger(self):
        # Mise en place bus ivy avec le pseudo rentré par le joueur
        if self._ivyBus is None:
            self._ivyBus = IvyBus(self._pseudo, self._game, self._window, True, "192.168.1.255")
            self._window.setAdapteurVue(self._ivyBus.getAdapteur_vue())
            self._window.frames['HebergerScreen'].getBoutonRetour().config(state='disabled')
        else:
            IvyStart()
        self._window.show_frame('HebergerScreen')

    # Validation du choix de mode de jeu où l'on cherche à rejoindre un HOST
    def validerRejoindre(self):
        if self._ivyBus is not None:
            IvyStart()
        self._window.show_frame('RejoindreScreen')

    def quitterLobby(self):
        if (self._ivyBus is not None):
            IvyStop()
        self._window.show_frame("GameModeScreen")

    # Validation de l'adresse entrée par le joueur qui essaye de joindre un HOST
    def validerAdresseJoindreHost(self, event):
        if self._ivyBus is None:
            self._ivyBus = IvyBus(self._pseudo, self._game, self._window, False, self._rejoindreScreen.getInputAdresseText())
            self._window.setAdapteurVue(self._ivyBus.getAdapteur_vue())
            if self._ivyBus is not None:
                self._rejoindreScreen.getInputAdresse().config(state='disabled')
                self._rejoindreScreen.getBoutonRetour().config(state='disabled')

    # Fonction de validation de la partie pour le joiner
    def validerJoueurPret(self):
        self._rejoindreScreen.montrerLabelPret()
        self._rejoindreScreen.desactiverBoutonPret()
        IvySendMsg("CMDVIEW | joueurPret | {0}".format(self._pseudo))

    # Fonction de validation de la partie par le HOST
    def validerPartie(self):
        self._game = Game(self._pseudo, self)
        # On initialise le Game
        self._game.setAdapteurModel(self._ivyBus.getAdapteur_model())
        # On récupère les paramètres de la partie
        self.isPartieCourte = self._hebergerScreen.varControleMode.get()
        if self.isPartieCourte == 'Standard':
            self.isPartieCourte = False
        else:
            self.isPartieCourte = True
        self.isCarteRetournee = self._hebergerScreen.varControleOption.get()
        if self.isCarteRetournee == 'Classique':
            self.isCarteRetournee = True
        else:
            self.isCarteRetournee = False
        self.nbBots = self._hebergerScreen._comboBoxAdversaires.get()[0]
        if self.nbBots == 'A':
            self.nbBots = int(0)
        else:
            self.nbBots = int(self.nbBots)
        print(self.nbBots)
        print(self.isPartieCourte)
        print(self.isCarteRetournee)
        self._game.initialiser(self.nbBots, self.isPartieCourte, self.isCarteRetournee)
        self._game.startTurn()
        # On met en place le GameScreen
        self._window.reset_screen("GameScreen")
        self.initGameScreen()
        # Si toutes ces conditions sont vérifiées alors le joueur peut poser sa carte
        for i in range(self._game.getNBJoueurs()):
            joueur = self._game.getPlayerByIndex(i)
            self._gameScreen.ajouterInfosJoueur(joueur.getJoueurInfos(), joueur.getPseudo())
            # On prévient les autres de passer à l'écran de Jeu
            IvySendMsg("CMDVIEW | prepareLabelsGameScreen | {0} | {1}".format(joueur.getJoueurInfos(), joueur.getPseudo()))
        self._gameScreen.updateLayout()
        # On update le label avec les infos de la partie
        if (self._game.started == True):
            if self._game.participantsTour[0].pseudo == self._game.name:
                self._gameScreen.setLabelInfoGame('C\'est à vous !')
            else:
                self._gameScreen.setLabelInfoGame('En attente des autres joueurs ...')
        self._window.show_frame("GameScreen")
        IvySendMsg("CMDVIEW | lancerPartie")

    def validerPartieSolo(self):
        # On reset la partie pour etre safe
        # self._game = Game()
        self._window.reset_screen("GameScreen")
        self.initGameScreen()
        # Gestion du joueur principal
        # pseudo = self._hebergerScreen._inputPseudo.get()
        # print('Pseudo du joueur principal %s' % pseudo)
        # self._mainPlayer = Joueur(pseudo)
        # self._game.addJoueur(self._mainPlayer)
        # self._gameScreen.afficherPseudoJoueurs(self._game.getJoueur(0).getPseudo())
        # Gestion des adversaires
        # nombreAdversaires = int(self._hebergerScreen.getSelectedItemComboBoxAdversaires()[0])
        # print('Nombre d\'adversaires choisi %s' % nombreAdversaires)
        # for i in range(0,nombreAdversaires):
        #     self._othersPlayers.append(Joueur(('Adversaire %d' % (i+1))))
        #     self._game.addJoueur(self._othersPlayers[i])
        #     self._gameScreen.afficherPseudoJoueurs((self._game.getJoueur(i+1).getPseudo()))
        # # On prépare la partie
        # self._game.distribuerCartes()
        # self._gameScreen.cacherElementInutiles()
        # self._gameScreen.afficherCartePile()
        # self._gameScreen.afficheCartes(self._game.getNBJoueurs())
        # On change d'écran
        self._window.show_frame("GameScreen")

    def moveCard(self, event):
        if self._gameScreen.getCartePile() is not None:
            print('move carte')
            self._gameScreen.getCanvas().coords(self._gameScreen.getCartePile(), event.x, event.y)

    # Sélection de la carte à jouer
    def selectionnerCarte(self, event):
        if (self._game.started == True) and self._game.currentState != self._game.stateRamasserPli:
            if self._game.participantsTour[0].pseudo == self._game.name:
                # self._gameScreen.setPeutJouer(True)
                print('entre dans selection carte')
                # self._cartePile = self._canvas.find_closest(event.x, event.y)[0] # Le 0 c'est car on prend la 1ere
                self._gameScreen._carteAJouer = self._gameScreen.getCanvas().find_withtag('carte_a_jouer')[0]

    # Sélection de la carte du Pli à récupérer
    def selectionnerCartePli(self, event):
        if (self._game.started == True) and self._game.currentState == self._game.stateRamasserPli:
            if(self._game.currentState.ramasseur.pseudo == self._game.name):
                print('entre dans selction carte Pli')
                # self._gameScreen._cartePliSelected = self._canvas.find_closest(event.x, event.y)[0]
                self._gameScreen._cartePliSelected = event.widget.find_withtag("current")[0]

    # Quand on relâche la carte à jouer ou à retirer
    def relacherCarte(self, event):
        if (self._gameScreen._carteAJouer is not None):
            self._gameScreen._carteAJouer = None
            enclosedObjects = self._gameScreen.getEnclosedObjectsZoneJeu()
            if len(enclosedObjects) > 0:
                for item in enclosedObjects:
                    if (item is self._gameScreen.getCartePile()):
                        print('carte a jouer relachee')
                        # Alors on montre la carte dans la zone de jeu
                        nomJoueur = self._game.name
                        if (self._statePremierCoupBataille == False):
                            carteAJouer = self._game.getPlayerByName(self._game.name).getCarteAJouer()
                            nom_carte = carteAJouer.getNomCarte()
                            fileNameCarteAJouer = carteAJouer.getNomCarteFormatFichier()
                            script_dir = os.path.dirname(__file__)
                            rel_path = "..\\images\\{0}.png"
                            abs_file_path = os.path.join(script_dir, rel_path)
                            abs_file_path = abs_file_path.format(fileNameCarteAJouer)
                        else:
                            nom_carte = "FACE_CACHEE_{0}".format(nomJoueur)
                            script_dir = os.path.dirname(__file__)
                            rel_path = "../images/face_cachee.png"
                            abs_file_path = os.path.join(script_dir, rel_path)
                        # On remet la carte face cachée à sa place d'origine et affiche la carte jouée
                        # On prévient que l'on vient de poser sa carte
                        infosCartePosee = "{0},{1},{2},{3},{4}".format(nomJoueur, abs_file_path, nom_carte, event.x, event.y)
                        if self._ivyBus.isHost() == True:
                            self._game.adapteur_model.notifyCurrentPlayerPlayed()
                            self._window._adapteur_vue.notifyCurrentPlayerPlayed(infosCartePosee)
                            self._window._adapteur_vue.notifyUpdateInfos(nomJoueur)
                            # Prise en compte des Bots
                            for i in range(len(self._actionsBots)):
                                actionBot = self._actionsBots[i].split(',')
                                action = actionBot[0]
                                nomBot = actionBot[1]
                                fileCarte = actionBot[2]
                                nom_carte = actionBot[3]
                                posX = actionBot[4]
                                posY = actionBot[5]
                                if (action == 'jouer'):
                                    infosCartePosee = "{0},{1},{2},{3},{4}".format(nomBot, fileCarte, nom_carte, posX, posY)
                                    # time.sleep(1)
                                    self._window._adapteur_vue.notifyCurrentPlayerPlayed(infosCartePosee)
                                elif action == 'ramasser':
                                    infosCarte = "{0},{1}".format(nomBot, nom_carte)
                                    # time.sleep(1)
                                    self._window._adapteur_vue.notifyCartePliRecuperee(infosCarte)
                        else:
                            self._window._adapteur_vue.askToHostToNotifyCurrentPlayerPlayed(infosCartePosee)
                            self._game.adapteur_model.askToHostToNotifyCurrentPlayerPlayed()
                            self._window._adapteur_vue.askToHostToNotifyUpdateInfos(nomJoueur)
                        self._gameScreen.setPeutJouer(False)
            self._gameScreen.resetPositionCartePile()
        elif (self._gameScreen._cartePliSelected is not None):
            print('carte pli relachee')
            isCarteRecuperee = False
            nom_carte = self._gameScreen.getCanvas().gettags(self._gameScreen._cartePliSelected)[0]
            enclosedObjects = self._gameScreen.getEnclosedObjectsZoneRetraitCarte()
            if len(enclosedObjects) > 0:
                for item in enclosedObjects:
                    if (item is self._gameScreen._cartePliSelected):
                        print('carte pli relachée dans zone retrait')
                        isCarteRecuperee = True
                        infosCarte = "{0},{1}".format(self._game.name, nom_carte)
                        if self._ivyBus.isHost() == True:
                            self._game.adapteur_model.notifyCarteRamassee(self._game.pli[0])
                            self._window._adapteur_vue.notifyCartePliRecuperee(infosCarte)
                        else:
                            self._game.adapteur_model.askToHostToNotifyCarteRamassee(self._game.pli[0])
                            self._window._adapteur_vue.askToHostToNotifyCartePliRecuperee(infosCarte)
            if isCarteRecuperee == False:
                infosCarteDeplacee = "{0},{1},{2}".format(nom_carte, event.x, event.y)
                if self._ivyBus.isHost():
                    self._window._adapteur_vue.notifyCarteDeplacement(infosCarteDeplacee)
                else:
                    self._window._adapteur_vue.askToHostToNotifyCarteDeplacement(infosCarteDeplacee)
            self._gameScreen._cartePliSelected = None

    def stockerInfosBots(self, action, nomBot, carteAJouer):
        nom_carte = carteAJouer.getNomCarte()
        print('Bot Carte' + nom_carte)
        fileNameCarteAJouer = carteAJouer.getNomCarteFormatFichier()
        script_dir = os.path.dirname(__file__)
        rel_path = "..\\images\\{0}.png"
        abs_file_path = os.path.join(script_dir, rel_path)
        abs_file_path = abs_file_path.format(fileNameCarteAJouer)
        gameScreen = self._window.frames['GameScreen']
        posX = randint(gameScreen.getXMinBot(), gameScreen.getXMaxBot())
        posY = randint(gameScreen.getYMinBot(), gameScreen.getYMaxBot())
        actionBot = "{0},{1},{2},{3},{4},{5}".format(action, nomBot, abs_file_path, nom_carte, posX, posY)
        self._actionsBots.append(actionBot)

    def gererPoseCarteBot(self, nomJoueur, carteAJouer):
        nom_carte = carteAJouer.getNomCarte()
        fileNameCarteAJouer = carteAJouer.getNomCarteFormatFichier()
        script_dir = os.path.dirname(__file__)
        print('Dossier ' + script_dir)
        rel_path = "..\\images\\{0}.png"
        abs_file_path = os.path.join(script_dir, rel_path)
        abs_file_path = abs_file_path.format(fileNameCarteAJouer)
        print('chemin fichier = ' + abs_file_path)
        gameScreen = self._window.frames['GameScreen']
        posX = randint(gameScreen.getXMinBot(), gameScreen.getXMaxBot())
        posY = randint(gameScreen.getYMinBot(), gameScreen.getYMaxBot())
        infosCartePosee = "{0},{1},{2},{3},{4}".format(nomJoueur, abs_file_path, nom_carte, posX, posY)
        gameScreen.showCarte(abs_file_path, nom_carte, posX, posY)
        IvySendMsg("CMDVIEW | cartePosee | {0}".format(infosCartePosee))
        print('Refresh Carte Jouee par bot')
