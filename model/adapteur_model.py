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
    def initGameForAllPlayers(self, game):
        for player in game.listeJoueurs:
            IvySendMsg("CMD | addPlayer | " + player.pseudo)
            for card in player.listeCartes:
                color = str(card.couleur)
                value = str(card.valeur)
                IvySendMsg("CMD | addCard | " + player.pseudo + " | " + color + " | " + value)

    # Analyse une commande
    def analyseCommand(self, command):
        command = command.split("|")
        actualCommand = command[1].strip()
        if actualCommand == "addPlayer": # Commande => Ajouter un nouveau joueur au jeu
            playerName = command[2].strip()
            self.addPlayerToGame(playerName)
        elif actualCommand == "addCard": # Commande => Ajouter une carte a un joueur
            playerName = command[2].strip()
            player = self.game.getPlayerByName(playerName)
            cardColor = command[3].strip()
            cardValue = command[4].strip()
            self.addCardToPlayer(player, cardColor, cardValue)

    # Crée un joueur et l'ajoute
    def addPlayerToGame(self, playerName):
        self.game.addJoueur(Joueur(playerName))

    # Crée une carte en fontion de la couleur et de la valeur décrite et l'ajoute au paquet du joueur
    def addCardToPlayer(self, player, color, value):
        carte = Carte.createCardFromStrings(color, value)
        player.addCarte(carte)

    def getPlayersName(self):
        return IvyGetApplicationList()
