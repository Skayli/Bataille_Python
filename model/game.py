from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from random import randint

class Game:

    def __init__(self):
        self.listeJoueurs = []
        self.listeCartes = []

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

    # Retourne le nombre de joueurs
    def getNBJoueurs(self):
        return len(self.listeJoueurs)

    # Initialise un paquet de carte, le mélange et le distribue aux listeJoueurs
    # de telle sorte que chacun possède le même nombre de cartes
    def distribuerCartes(self):
        self.initialiserListeCartes()
        self.melangerCartes()

        for j in self.listeJoueurs:
            j.initialiser()

        while(len(self.listeCartes) >= len(self.listeJoueurs)):
            for j in self.listeJoueurs:
                j.addCarte(self.listeCartes.pop(0))

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
        print("\n".join(str(j) for j in self.listeJoueurs))

    def printListeCartes(self):
        print("\n".join(str(e) for e in self.listeCartes))
