from ivy.std_api import *
from tkinter import *
from PIL import Image,ImageTk

from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from model.game import *

import time
import re

class Adapteur_vue:

    def __init__(self):
        pass

    def setCadre(self, cadre):
        self._cadre = cadre

    def isCommand(self, msg):
        return str(msg).startswith("CMDVIEW |")

    def prepareCommand(self, command):
        self._cadre.addQueue(command)

    #Analyse une commande
    def analyseCommand(self, command):
        command = command.split("|")
        actualCommand = command[1].strip()
        # Mets à jour les labels des joueurs du Lobby HebergerScreen
        if actualCommand == "updateLabelsJoueursHebergerScreen":
            agentName = command[2].strip()
            # On refresh la page du host
            hebergerScreen = self._cadre.frames['HebergerScreen']
            labelsJoueurs = hebergerScreen.getLabelsJoueurs()
            msg = ("Le joueur %s a rejoint le lobby" % agentName)
            labelsJoueurs.append(Label(hebergerScreen, text=msg, font=hebergerScreen._helv20))
            hebergerScreen.updateLabelsJoueurs()
            # Mettre à jour les infos sur les joueurs humains et sur le bouton Jouer
            hebergerScreen.incrementerNombreJoueursHumains()
            hebergerScreen.updateEtatBoutonJouer()
        elif actualCommand == "updateLabelHostRejoindreScreen":
            agentName = command[2].strip()
            rejoindreScreen = self._cadre.frames['RejoindreScreen']
            labelHost = rejoindreScreen.setLabelHostText(("Vous êtes connecté à la partie de %s" % agentName))
            rejoindreScreen.montrerBoutonPret()
        elif actualCommand == "joueurPret":
            playerName = command[2].strip()
            hebergerScreen = self._cadre.frames['HebergerScreen']
            for labelJoueur in hebergerScreen.getLabelsJoueurs():
                m = re.search('Le joueur (.+?) a rejoint le lobby', labelJoueur.cget('text'))
                if m:
                    found = m.group(1)
                    newText = "{0} => {1} est prêt !".format(labelJoueur.cget('text'), found)
                    labelJoueur.configure(text=newText)
                    # Mettre à jour les infos sur les joueurs humains et sur le bouton Jouer
                    hebergerScreen.incrementerNombreJoueursHumainsPrets()
                    hebergerScreen.updateEtatBoutonJouer()
                    # Ajouter le nom du Joueur
                    hebergerScreen.ajouterNomJoueur(found)
                    break

    # Crée un joueur et l'ajoute
    def addPlayerToGame(self, playerName):
        self.game.addJoueur(Joueur(playerName))

    # Crée une carte en fontion de la couleur et de la valeur décrite et l'ajoute au paquet du joueur
    def addCardToPlayer(self, player, color, value):
        carte = Carte.createCardFromStrings(color, value)
        player.addCarte(carte)

    def getPlayersName(self):
        return IvyGetApplicationList()