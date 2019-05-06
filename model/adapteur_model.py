from ivy.std_api import *

from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from model.game import *

import time

class Adapteur_model:

    def __init__(self):
        pass

    def setGame(self, game):
        self.game = game

    def isCommand(self, msg):
        return str(msg).startswith("CMD |")

    # Initialise le jeu pour tous les joueurs
    def initGameForAllPlayers(self):
        for player in self.game.listeJoueurs:
            IvySendMsg("CMD | startGame")
            IvySendMsg("CMD | addPlayer | " + player.pseudo)
            for card in player.listeCartes:
                color = str(card.couleur)
                value = str(card.valeur)
                IvySendMsg("CMD | addCardToPlayer | " + player.pseudo + " | " + color + " | " + value)

    # Initialise les participants au tour
    def setPlayerTurnOrder(self):
        IvySendMsg("CMD | resetListeParticipantsTour")
        for player in self.game.participantsTour:
            print("Ajout de " + player.pseudo + " A la liste des joueur au tour")
            IvySendMsg("CMD | addParticipantTour | " + player.pseudo)

    # HOST - Notifie tout le monde que le joueur courant a joué son coup
    def notifyCurrentPlayerPlayed(self):
        j = self.game.participantsTour.pop(0)
        print("[Adapteur_model] A joué : " + j.pseudo)
        IvySendMsg("CMD | currentPlayerPlayed")

        if self.game.currentState.actionsTerminees():
            self.game.currentState.handleTurn()

    # Envoie un message à l'hote de dire à tous que le joueur courrant a joué son coup
    def askToHostToNotifyCurrentPlayerPlayed(self):
        print("[Adapteur_model] J'AI JOUE")
        IvySendMsg("CMD | sendNotificationCurentPlayerPlayed")

    # Notifie tout le monde de retirer la carte du pli et de l'ajouté au paquet du joueur
    def notifyCarteRamassee(self, carte):
        color = str(carte.couleur)
        value = str(carte.valeur)
        carte = self.game.getCardFromPli(CouleurCarte[color], ValeurCarte[value])
        self.game.pli.remove(carte)
        self.game.currentState.ramasseur.addCarte(carte)

        print("[Adapteur_model] PLI : ")
        for carte in self.game.pli:
            print(str(carte))
        print("[Adapteur_model] JOUEURS : ")
        for j in self.game.listeJoueurs:
            print(str(j))
        IvySendMsg("CMD | cartePliRamassee | " + color + " | " + value)

        if self.game.currentState.actionsTerminees():
            self.game.currentState.handleTurn()

    def askToHostToNotifyCarteRamassee(self, carte):
        color = str(carte.couleur)
        value = str(carte.valeur)
        IvySendMsg("CMD | sendNotificationCarteRamasse | " + color + " | " + value)

    # Notifie tout le monde qu'il faut retirer la carte jouée du paquet du joueur pour la rajouter au pli
    def retirerCarteJouerEtAjouterAuPli(self, player):
        IvySendMsg("CMD | removePlayedCard | " + player.pseudo)

    # Notifie tout le monde de definir le joueur en tant que ramasseur
    def setRamasseur(self, joueur):
        IvySendMsg("CMD | setRamasseur | " + joueur.pseudo)

    # Notifie tout le monde de définir l'état courant à "Ramasser le pli"
    def setGameStateToRamasserPli(self):
        IvySendMsg("CMD | setGameStateToRamasserPli")

    # Notifie tout le monde définir l'état courant à "Tour normal"
    def setGameStateToTourNormal(self):
        IvySendMsg("CMD | setGameStateToTourNormal")

    # Notifie tout le monde de définir l'état courant à "Premier coup Bataille"
    def setGameStateToPremierCoupBataille(self):
        IvySendMsg("CMD | setGameStateToPremierCoupBataille")

    # Notifie tout le monde de définir l'état courant à "Deuxieme coup Bataille"
    def setGameStateToDeuxiemeCoupBataille(self):
        IvySendMsg("CMD | setGameStateToDeuxiemeCoupBataille")

    # Analyse une commande
    def analyseCommand(self, command):
        command = command.split("|")
        actualCommand = command[1].strip()
        if actualCommand == "addPlayer": # Commande => Ajouter un nouveau joueur au jeu
            playerName = command[2].strip()
            self.addPlayerToGame(playerName)
        elif actualCommand == "addCardToPlayer": # Commande => Ajouter une carte a un joueur
            playerName = command[2].strip()
            player = self.game.getPlayerByName(playerName)
            cardColor = command[3].strip()
            cardValue = command[4].strip()
            self.addCardToPlayer(player, cardColor, cardValue)
        elif actualCommand == "startGame":
            self.game.started = True
        elif actualCommand == "resetListeParticipantsTour":
            self.game.participantsTour = []
        elif actualCommand == "addParticipantTour":
            print("[adapteur_model] AJOUT PARTICIPANT AU TOUR : " + command[2])
            playerName = command[2].strip()
            player = self.game.getPlayerByName(playerName)
            self.game.participantsTour.append(player)
        elif actualCommand == "currentPlayerPlayed":
            self.game.participantsTour.pop(0)
        elif actualCommand == "sendNotificationCurentPlayerPlayed":
            self.notifyCurrentPlayerPlayed()
        elif actualCommand == "removePlayedCard":
            playerName = command[2].strip()
            player = self.game.getPlayerByName(playerName)
            self.game.pli.append(player.listeCartes.pop(0))
        elif actualCommand == "setRamasseur":
            playerName = command[2].strip()
            player = self.game.getPlayerByName(playerName)
            self.game.stateRamasserPli.setRamasseur(player)
        elif actualCommand == "setGameStateToRamasserPli":
            print("[Adapteur_model] passage au mode RAMASSER")
            self.game.currentState = self.game.stateRamasserPli
            self.game.currentState.printStateName()
        elif actualCommand == "sendNotificationCarteRamasse":
            cardColor = command[2].strip()
            cardValue = command[3].strip()
            carte = self.game.getCardFromPli(CouleurCarte[cardColor], ValeurCarte[cardValue])
            self.notifyCarteRamassee(carte)
        elif actualCommand == "cartePliRamassee":
            cardColor = command[2].strip()
            cardValue = command[3].strip()
            carte = self.game.getCardFromPli(CouleurCarte[cardColor], ValeurCarte[cardValue])
            self.game.pli.remove(carte)
            self.game.currentState.ramasseur.addCarte(carte)
            print("[Adapteur_model] PLI : ")
            for carte in self.game.pli:
                print(str(carte))
            print("[Adapteur_model] JOUEURS : ")
            for j in self.game.listeJoueurs:
                print(str(j))
        elif actualCommand == "setGameStateToTourNormal":
            print("BACK TO STATE NORMAL")
            self.game.currentState = self.game.stateTourNormal
        elif actualCommand == "setGameStateToPremierCoupBataille":
            self.game.currentState = self.game.statePremierCoupBataille
        elif actualCommand == "setGameStateToDeuxiemeCoupBataille":
            self.game.currentState = self.game.stateDeuxiemeCoupBataille

    # Crée un joueur et l'ajoute
    def addPlayerToGame(self, playerName):
        self.game.addJoueur(Joueur(playerName))

    # Crée une carte en fontion de la couleur et de la valeur décrite et l'ajoute au paquet du joueur
    def addCardToPlayer(self, player, color, value):
        carte = Carte.createCardFromStrings(color, value)
        player.addCarte(carte)

    def getPlayersName(self):
        return IvyGetApplicationList()
