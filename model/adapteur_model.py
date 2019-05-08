from ivy.std_api import *

from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from model.bot import *
from model.game import *

import time
import os

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
            print("[Adapteur_model] Ajout à la liste des joueur au tour : " + str(player))
            IvySendMsg("CMD | addParticipantTour | " + player.pseudo)

    # HOST - Notifie tout le monde que le joueur courant a joué son coup
    def notifyCurrentPlayerPlayed(self):
        j = self.game.participantsTour.pop(0)
        print("[Adapteur_model] " + j.pseudo + " a joué " + str(j.listeCartes[0]))
        IvySendMsg("CMD | currentPlayerPlayed")

        if self.game.currentState.actionsTerminees():
            self.game.currentState.handleTurn()
        elif isinstance(self.game.participantsTour[0], Bot):
            # time.sleep(self.game.botWaitTime)
            nomJoueur = self.game.participantsTour[0].getPseudo()
            carteAJouer = self.game.participantsTour[0].getCarteAJouer()
            action = 'jouer'
            self.game.controller.stockerInfosBots(action, nomJoueur, carteAJouer)
            self.notifyCurrentPlayerPlayed()

    # HOST - Notifie tout le monde d'ajouter les cartes à la liste du joueur
    def addPlayerCardToScore(self, player):
        while(len(player.listeCartes) > 0):
            player.listeScore.append(player.listeCartes.pop(0))
            IvySendMsg("CMD | addPlayerCardToScore | " + player.pseudo)


    # Envoie un message à l'hote de dire à tous que le joueur courrant a joué son coup
    def askToHostToNotifyCurrentPlayerPlayed(self):
        IvySendMsg("CMD | sendNotificationCurentPlayerPlayed")

    # Notifie tout le monde de retirer la carte du pli et de l'ajouté au paquet du joueur
    def notifyCarteRamassee(self, carte):
        color = str(carte.couleur)
        value = str(carte.valeur)
        carte = self.game.getCardFromPli(CouleurCarte[color], ValeurCarte[value])
        self.game.pli.remove(carte)
        if self.game.court == False:
            self.game.currentState.ramasseur.addCarte(carte)
        else:
            self.game.currentState.ramasseur.addCarteToScore(carte)

        IvySendMsg("CMD | cartePliRamassee | " + color + " | " + value)

        if self.game.currentState.actionsTerminees():
            self.game.currentState.handleTurn()
        elif isinstance(self.game.currentState.ramasseur, Bot):
            # time.sleep(self.game.botWaitTime)
            nomJoueur = self.game.currentState.ramasseur.getPseudo()
            carteAJouer = self.game.pli[0]
            action = 'ramasser'
            self.game.controller.stockerInfosBots(action, nomJoueur, carteAJouer)
            self.notifyCarteRamassee(self.game.pli[0])

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

    def setGameStateToFinPartie(self):
        IvySendMsg("CMD | setGameStateToFinPartie")

    # Analyse une commande de type "CMD | Commande | PARAMS | etc..."
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
        elif actualCommand == "setGameStateToTourNormal":
            self.game.currentState = self.game.stateTourNormal
        elif actualCommand == "setGameStateToPremierCoupBataille":
            self.game.currentState = self.game.statePremierCoupBataille
        elif actualCommand == "setGameStateToDeuxiemeCoupBataille":
            self.game.currentState = self.game.stateDeuxiemeCoupBataille
        elif actualCommand == "setGameStateToFinPartie":
            self.game.currentState = self.game.stateFinPartie
        elif actualCommand == "addPlayerCardToScore":
            playerName = command[2].strip()
            player = self.game.getPlayerByName(playerName)
            player.listeScore.append(player.listeCartes.pop(0))

    # Crée un joueur et l'ajoute
    def addPlayerToGame(self, playerName):
        self.game.addJoueur(Joueur(playerName))

    # Crée une carte en fontion de la couleur et de la valeur décrite et l'ajoute au paquet du joueur
    def addCardToPlayer(self, player, color, value):
        carte = Carte.createCardFromStrings(color, value)
        player.addCarte(carte)

    def getPlayersName(self):
        return IvyGetApplicationList()
