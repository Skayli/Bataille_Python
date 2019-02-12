from classes.couleurCarte import *
from classes.valeurCarte import *
from classes.carte import *
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
    def jouerTour(self):
        # 1ère Etape : recherche des batailles

        sizeListe = len(self.listeJoueurs)
        battlePatners = []

        for i in range(0, sizeListe):
            mustBattle = False
            for j in range(i+1, sizeListe):
                if(self.listeJoueurs[i].getCarteAJouer() == self.listeJoueurs[j].getCarteAJouer()):
                    mustBattle = True

            if mustBattle:
                battlePatners.append(self.listeJoueurs[i])

        print(battlePatners)

        # print("\nRésultat du tour")
        # print(listeGagnants)
        # print(listeCartesEnJeu)


    def printListeJoueurs(self):
        print("\n".join(str(j) for j in self.listeJoueurs))

    def printListeCartes(self):
        print("\n".join(str(e) for e in self.listeCartes))
