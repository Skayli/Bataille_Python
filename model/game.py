from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from random import randint
from model.states.stateTourNormal import *
from model.states.stateRamasserPli import *
from model.states.statePremierCoupBataille import *
from model.states.stateDeuxiemeCoupBataille import *

class Game:

    def __init__(self, name):
        self.listeJoueurs = []
        self.listeCartes = []
        self.pli = []
        self.participantsBataille = []
        self.started = False
        self.name = name

        self.participantsTour = []

        self.stateTourNormal = StateTourNormal(self)
        self.statePremierCoupBataille = StatePremierCoupBataille(self)
        self.stateDeuxiemeCoupBataille = StateDeuxiemeCoupBataille(self)
        self.stateRamasserPli = StateRamasserPli(self)

        self.currentState = self.stateTourNormal

    # Initialise un paquet de carte, le mélange et le distribue aux listeJoueurs
    # de telle sorte que chacun possède le même nombre de cartes
    def initialiser(self):
        self.initialiserListeCartes()
        self.melangerCartes()
        self.createPlayers()

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

    def startTurn(self):
        if self.isFinished():
            print("PARTIE TERMINEE")
        else:
            self.currentState.initialiser()

    # A COMPLETER
    def isFinished(self):
        return False

    def playRound(self):
        print("toast")

        # Definir si on est dans une bataille ou pas
        if not self.battle : # Tour normal
            listeJoueurs = self.getListeJoueurPouvantJouer()

            # Detection bataille
            battleCard = None

            for j1 in listeJoueurs:
                for j2 in listeJoueurs:
                    if j1 != j2 and j1.getCarteAJouer().valeur ==  j2.getCarteAJouer().valeur:
                        if battleCard == None or battleCard < j1.getCarteAJouer():
                            battleCard = j1.getCarteAJouer()


            if battleCard != None:
                # Ajout des joueurs participants à la bataille
                self.participantsBataille = []

                for j in listeJoueurs:
                    if j.getCarteAJouer().valeur == battleCard.valeur:
                        self.participantsBataille.append(j)

                # On enlève les joueurs ne pouvant plus jouer
                for j in self.participantsBataille:
                    if not self.canPlayBattle(j):
                        self.participantsBataille.remove(j)

                if len(self.participantsBataille) >= 2:
                    self.battle = True

                # Ajout des cartes jouées au pli
                for joueur in listeJoueurs:
                    self.pli.append(joueur.listeCartes.pop(0))


    def oneRound(self, listeJoueurs):
        # Etape 1 : Chercher les batailles
        battleCard = None

        for j1 in listeJoueurs:
            for j2 in listeJoueurs:
                if j1 != j2 and j1.getCarteAJouer().valeur ==  j2.getCarteAJouer().valeur:
                    if battleCard == None or battleCard < j1.getCarteAJouer():
                        battleCard = j1.getCarteAJouer()

        # Fin etape 1

        # ----------------------------------------------------------------------------- #

        # Etape 2 : Gérer la bataille ou finir le tour

        # Etape 2.1 : Gérer s'il y a bataille
        if(battleCard != None):
            # Etape 2.1.1 Ajout des joueurs participants à la bataille
            self.participantsBataille = []

            for j in listeJoueurs:
                if j.getCarteAJouer().valeur == battleCard.valeur:
                    self.participantsBataille.append(j)

            # Etape 2.1.2 Ajout des cartes en jeu au pli : les cartes joués par les joueurs pouvant joué au début du tour
            for j in listeJoueurs:
                self.pli.append(j.listeCartes.pop(0))

            print("BATAILLE de " + str(battleCard.valeur))
            for j in self.participantsBataille:
                if not self.isOver(j):
                    self.pli.append(j.listeCartes.pop(0))
                    print(str(j))

            print("-------------------")
            return False

        # Etape 2.2 : Finir le tour
        else:
            #Etape 2.2.1 : Trouver le gagnant
            gagnant = listeJoueurs[0]

            for j in listeJoueurs:
                if j.getCarteAJouer() > gagnant.getCarteAJouer():
                    gagnant = j

            for j in listeJoueurs:
                print(j.getCarteAJouer())
                self.pli.append(j.listeCartes.pop(0))

            gagnant.listeCartes.extend(self.pli)
            print("GAGNANT SEUL :\n" + str(j))

            # Fin d'un tour de jeu : on reset pli et liste participantsBataille
            self.pli = []
            self.participantsBataille = []

            return True

        # Fin etape 2

    # Effectue un tour de jeu
    def jouerTour(self, listeJoueurs = None, listeCartesEnJeu = None):

        if listeJoueurs == None:
            listeJoueurs = self.listeJoueurs

        if listeCartesEnJeu == None:
            listeCartesEnJeu = []

        # Chercher les batailles
        battleCard = None

        for j1 in listeJoueurs:
            for j2 in listeJoueurs:
                if j1 != j2 and j1.getCarteAJouer().valeur ==  j2.getCarteAJouer().valeur:
                    if battleCard == None or battleCard < j1.getCarteAJouer():
                        battleCard = j1.getCarteAJouer()


        if(battleCard != None):
            participantsBataille = []

            for j in listeJoueurs:
                if j.getCarteAJouer().valeur == battleCard.valeur:
                    participantsBataille.append(j)

            for j in listeJoueurs:
                listeCartesEnJeu.append(j.listeCartes.pop(0))
                if j in participantsBataille:
                    listeCartesEnJeu.append(j.listeCartes.pop(0))  #carte retournée du joueur

            self.jouerTour(participantsBataille, listeCartesEnJeu)

        else:
            # Trouver le gagant et lui donner les cartes en jeu
            gagnant = listeJoueurs[0]

            for j in listeJoueurs:
                if j.getCarteAJouer() > gagnant.getCarteAJouer():
                    gagnant = j

            for j in listeJoueurs:
                print(j.getCarteAJouer())
                listeCartesEnJeu.append(j.listeCartes.pop(0))


            gagnant.listeCartes.extend(listeCartesEnJeu)
            print("GAGNANT SEUL :\n" + str(j))


    def printListeJoueurs(self):
        if(len(self.listeJoueurs) == 0):
            print("Aucun joueur n'a encore été ajouté")
        else:
            print("\n".join(str(j) for j in self.listeJoueurs))

    def printListeCartes(self):
        print("\n".join(str(e) for e in self.listeCartes))

    def getListeJoueurPouvantJouer(self):
        listeJ = []
        for j in self.listeJoueurs:
            if not self.isOver(j):
                listeJ.append(j)

        return listeJ

    def canPlayBattle(self, player):
        return player.getNbCartes() >= 2

    # Créé les joueurs en fonction des noms des applications connectées
    def createPlayers(self):
        self.addJoueur(Joueur(self.name))
        listeNomJoueurs = self.adapteur_model.getPlayersName()
        for name in listeNomJoueurs:
            self.addJoueur(Joueur(name))

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
