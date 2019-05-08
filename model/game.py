from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from model.bot import *
from random import randint
from model.states.stateTourNormal import *
from model.states.stateRamasserPli import *
from model.states.statePremierCoupBataille import *
from model.states.stateDeuxiemeCoupBataille import *
from model.states.stateFinPartie import *

class Game:

    def __init__(self, name, controller):
        self.listeJoueurs = []
        self.listeCartes = []
        self.pli = []
        self.participantsBataille = []
        self.started = False
        self.name = name
        self.botWaitTime = 0.5
        self.controller = controller

        self.participantsTour = []

        self.stateTourNormal = StateTourNormal(self)
        self.statePremierCoupBataille = StatePremierCoupBataille(self)
        self.stateDeuxiemeCoupBataille = StateDeuxiemeCoupBataille(self)
        self.stateRamasserPli = StateRamasserPli(self)
        self.stateFinPartie = StateFinPartie(self)

        self.currentState = self.stateTourNormal

        self.listeNomsBot = ["Bot Aniste", "Bot Ox", "Bot Swana"]

    # Initialise un paquet de carte, le mélange et le distribue aux listeJoueurs
    # de telle sorte que chacun possède le même nombre de cartes
    def initialiser(self, nbBots, isShort, retourner):
        self.court = isShort
        self.retourner = retourner

        print("Court : " + str(self.court))
        print("Retourner : " + str(self.retourner))
        print("Nombre de bots : " + str(nbBots))

        self.initialiserListeCartes()
        self.melangerCartes()
        self.createPlayers(nbBots)

        for j in self.listeJoueurs:
            j.initialiser()

        while(len(self.listeCartes) >= len(self.listeJoueurs)):
            for j in self.listeJoueurs:
                j.addCarte(self.listeCartes.pop(0))

        self.started = True
        self.adapteur_model.initGameForAllPlayers()

    # Initialise un paquet de carte complet
    def initialiserListeCartes(self):
        self.listeCartes = []

        for couleur in CouleurCarte:
            for valeur in ValeurCarte:
                self.listeCartes.append(Carte(couleur, valeur))

    #  Melange le paquet de cartes du jeu
    def melangerCartes(self):
        for i in range(0, len(self.listeCartes)-1):
            randomIndex = randint(0, len(self.listeCartes)-1)
            tmp = self.listeCartes[randomIndex]
            self.listeCartes[randomIndex] = self.listeCartes[i]
            self.listeCartes[i] = tmp

    # Ajoute un joueur s'il n'est pas deja dans la liste ou si la longueur est < à 4
    def addJoueur(self, joueur):
        if joueur not in self.listeJoueurs and len(self.listeJoueurs) < 4:
            self.listeJoueurs.append(joueur)
            return True

        return False

    # Retire un joueur de la liste des joueurs
    def removeJoueur(self, name):
        for joueur in self.listeJoueurs:
            if joueur.pseudo == name:
                self.listeJoueurs.remove(joueur)
                return True

        return False

    # Retourne le nombre de joueurs
    def getNBJoueurs(self):
        return len(self.listeJoueurs)

    # Check si un joueur ne peut plus jouer
    def isOver(self, joueur):
        return joueur.getNbCartes() == 0

    # Lance le tour  d'action, défini par l'état actuel du jeu
    def startTurn(self):
        self.currentState.initialiser()

    # Check si la partie est terminée
    def isFinished(self):
        if self.court: # Verifie si au moins 2 joueurs peuvent jouer
            return len(self.getListeJoueurPouvantJouerUnCoup()) < 2
        else: # Verifie si le nombre de carte non distribuées + les nombre de carte d'un joueur = 52
            for j in self.listeJoueurs:
                if (len(self.listeCartes) + len(j.listeCartes)) == 52:
                    return True
            return False

    def printListeJoueurs(self):
        if(len(self.listeJoueurs) == 0):
            print("Aucun joueur n'a encore été ajouté")
        else:
            print("\n".join(str(j) for j in self.listeJoueurs))

    def printListeCartes(self):
        print("\n".join(str(e) for e in self.listeCartes))

    def getListeJoueurPouvantJouerUnCoup(self):
        listeJ = []
        for j in self.listeJoueurs:
            if not self.isOver(j):
                listeJ.append(j)
        return listeJ

    def canPlayBattle(self, player):
        if self.retourner == True: # En mode "retourner" il faut poser 2 cartes : cachée puis visible
            return player.getNbCartes() >= 2
        else:
            return player.getNbCartes() >= 1 # Sinon, au moins 1

    # Créé les joueurs en fonction des noms des applications connectées
    def createPlayers(self, nbBots):
        self.addJoueur(Joueur(self.name))
        listeNomJoueurs = self.adapteur_model.getPlayersName()
        for name in listeNomJoueurs:
            self.addJoueur(Joueur(name))

        for i in range (0, nbBots):
            self.addJoueur(Bot(self.listeNomsBot[i]))

    def setAdapteurModel(self, adapteur_model):
        self.adapteur_model = adapteur_model
        adapteur_model.setGame(self)

    def getPlayerByName(self, name):
        for player in self.listeJoueurs:
            if player.pseudo == name:
                return player
        return None

    def getCardFromPli(self, color, value):
        for card in self.pli:
            if (card.couleur == color) and (card.valeur == value):
                return card
        return None

    def getPlayerByIndex(self, index):
        if index < self.getNBJoueurs():
            return self.listeJoueurs[index]
        return None

    def getWinner(self):
        gagnant = []
        if self.court == True: # Le gagnant est celui qui a le plus de cartes dans sa listeScore. Il peut y avoir plusieurs gagnants
            max = 0
            for joueur in self.listeJoueurs:
                if len(joueur.listeScore) > max:
                    gagnant = []
                    max = len(joueur.listeScore)
                    gagnant.append(joueur)
                elif len(joueur.listeScore) == max:
                    gagnant.append(joueur)
            return gagnant
        else: # Il n'y aura qu'un seul gagant : le seul qui a encore des cartes
            for joueur in self.listeJoueurs:
                if (len(self.listeCartes) + len(joueur.listeCartes)) == 52:
                    gagnant.append(joueur)
                    break
            return gagnant
