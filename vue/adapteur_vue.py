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

    def notifyCurrentPlayerPlayed(self, infosCartePosee):
        self.gererPoseCarte(infosCartePosee)
        IvySendMsg("CMDVIEW | cartePosee | {0}".format(infosCartePosee))

    def askToHostToNotifyCurrentPlayerPlayed(self, infosCartePosee):
        IvySendMsg("CMDVIEW | askToHostToNotifyCurrentPlayerPlayed | {0}".format(infosCartePosee))

    def notifyCarteDeplacement(self, infosCarteDeplacee):
        self.gererDeplacementCarte(infosCarteDeplacee)
        IvySendMsg("CMDVIEW | notifyCarteDeplacement | {0}".format(infosCarteDeplacee))

    def askToHostToNotifyCarteDeplacement(self, infosCarteDeplacee):
        IvySendMsg("CMDVIEW | askToHostToNotifyCarteDeplacement | {0}".format(infosCarteDeplacee))

    def notifyCartePliRecuperee(self, infoCarte):
        self.gererRecuperationCartePli(infoCarte)
        IvySendMsg("CMDVIEW | notifyCartePliRecuperee | {0}".format(infoCarte))

    def askToHostToNotifyCartePliRecuperee(self, infoCarte):
        IvySendMsg("CMDVIEW | askToHostToNotifyCartePliRecuperee | {0}".format(infoCarte))

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
            labelsJoueurs.append(Label(hebergerScreen, text=msg, font=hebergerScreen._helv20, bg='linen'))
            hebergerScreen.updateLabelsJoueurs()
            # Mettre à jour les infos sur les joueurs humains et sur le bouton Jouer
            hebergerScreen.incrementerNombreJoueursHumains()
            hebergerScreen.updateComboBoxBots()
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
                    if found == playerName:
                        newText = "{0} => {1} est prêt !".format(labelJoueur.cget('text'), found)
                        labelJoueur.configure(text=newText ,bg='pale green')
                        # Mettre à jour les infos sur les joueurs humains et sur le bouton Jouer
                        hebergerScreen.incrementerNombreJoueursHumainsPrets()
                        hebergerScreen.updateEtatBoutonJouer()
                        # Ajouter le nom du Joueur
                        hebergerScreen.ajouterNomJoueur(found)
                        break
        elif actualCommand == "prepareLabelsGameScreen":
            gameScreen = self._cadre.frames['GameScreen']
            playerInfos = command[2].strip()
            playerName = command[3].strip()
            gameScreen.ajouterInfosJoueur(playerInfos, playerName)
        elif actualCommand == "lancerPartie":
            gameScreen = self._cadre.frames['GameScreen']
            game = self._cadre._controller._game
            gameScreen.updateLayout()
            if (game.started == True) and game.currentState != game.stateRamasserPli:
                if game.participantsTour[0].pseudo == game.name:
                    gameScreen.setLabelInfoGame('C\'est à vous !')
                else:
                    gameScreen.setLabelInfoGame('En attente des autres joueurs ...')
            self._cadre.show_frame("GameScreen")
        elif actualCommand == "cartePosee":
            self.gererPoseCarte(command[2].strip())
        elif actualCommand == "askToHostToNotifyCurrentPlayerPlayed":
            self.notifyCurrentPlayerPlayed(command[2].strip())
        elif actualCommand == "notifyCarteDeplacement":
            self.gererDeplacementCarte(command[2].strip())
        elif actualCommand == "askToHostToNotifyCarteDeplacement":
            self.notifyCarteDeplacement(command[2].strip())
        elif actualCommand == "notifyCartePliRecuperee":
            self.gererRecuperationCartePli(command[2].strip())
        elif actualCommand == "askToHostToNotifyCartePliRecuperee":
            self.notifyCartePliRecuperee(command[2].strip())

    def gererPoseCarte(self, infosCartePosee):
        cartePosee = infosCartePosee.split(",")
        nomJoueur = cartePosee[0]
        fileName = cartePosee[1]
        nomCarte = cartePosee[2]
        posX = cartePosee[3]
        posY = cartePosee[4]
        gameScreen = self._cadre.frames['GameScreen']
        gameScreen.showCarte(fileName, nomCarte, posX, posY)
        # on update le labelInfoGame
        game = self._cadre._controller._game
        joueur = self._cadre._controller._game.getPlayerByName(nomJoueur)
        if (game.started == True):
            # Si tout n'est pas terminé
            if game.currentState == game.stateTourNormal:
                gameScreen.updateLabelJoueur(nomJoueur, "{0} : Nombre de cartes restantes {1}".format(nomJoueur, joueur.getNbCartes()-1))
                if game.participantsTour[0].pseudo == game.name:
                    gameScreen.setLabelInfoGame('C\'est à vous !')
                else:
                    gameScreen.setLabelInfoGame('En attente des autres joueurs ...')
            # Si tour terminé et vainqueur
            elif game.currentState == game.stateRamasserPli:
                gameScreen.updateLabelJoueur(nomJoueur, "{0} : Nombre de cartes restantes {1}".format(nomJoueur, joueur.getNbCartes()))
                if(game.currentState.ramasseur.pseudo == game.name):
                    gameScreen.setLabelInfoGame('Vous avez gagné le tour, veuillez ramasser les cartes')
                else:
                    gameScreen.setLabelInfoGame('{0} a gagné le tour, en attente du ramassage de cartes...'.format(nomJoueur))
            # Si tour terminé et Bataille premier coup
            elif game.currentState == game.statePremierCoupBataille:
                self._cadre._controller._statePremierCoupBataille = True
                if game.participantsTour[0].pseudo == game.name:
                    gameScreen.setLabelInfoGame('Bataille ! Posez la carte face cachée !')
                else:
                    gameScreen.setLabelInfoGame('Bataille ! En attente des autres joueurs...')
            # Si tour terminé et Bataille deuxième coup
            elif game.currentState == game.stateDeuxiemeCoupBataille:
                self._cadre._controller._statePremierCoupBataille = False
                if game.participantsTour[0].pseudo == game.name:
                    gameScreen.setLabelInfoGame('Bataille ! Posez la carte')
                else:
                    gameScreen.setLabelInfoGame('Bataille ! En attente des autres joueurs...')

    def gererDeplacementCarte(self, infosCarteDeplacee):
        carte = infosCarteDeplacee.split(",")
        nom_carte = carte[0]
        posX = carte[1]
        posY = carte[2]
        gameScreen = self._cadre.frames['GameScreen']
        gameScreen.deplacerCarte(nom_carte, posX, posY)

    def gererRecuperationCartePli(self, infoCarte):
        infos = infoCarte.split(",")
        nom_joueur = infos[0]
        nom_carte = infos[1]
        gameScreen = self._cadre.frames['GameScreen']
        game = self._cadre._controller._game
        gameScreen.getCanvas().delete(nom_carte)
        del gameScreen._dict_imagesCartes[nom_carte]
        # Mise à jour des labels infos sur les joueurs
        joueur = self._cadre._controller._game.getPlayerByName(nom_joueur)
        gameScreen.updateLabelJoueur(nom_joueur, joueur.getJoueurInfos())
        # Vérification de si on a terminé le ramassage
        if (game.started == True) and game.currentState != game.stateRamasserPli:
            if game.participantsTour[0].pseudo == game.name:
                gameScreen.setLabelInfoGame('Ramassage terminé, c\'est à vous !')
            else:
                gameScreen.setLabelInfoGame('Ramassage terminé, en attente des autres joueurs...')
