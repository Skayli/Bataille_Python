from model.couleurCarte import *
from model.valeurCarte import *

class Carte:

    def __init__(self, couleur, valeur):
        self.valeur = valeur
        self.couleur = couleur

    def __repr__(self):
        return "[Carte => " + str(self.valeur) + " de " + str(self.couleur) + "]"

    # Vérifie si les deux cartes ont la meme couleur (pique, trefle, coeur, carreau)
    def ontLaMemeCouleur(c1, c2):
        return c1.couleur == c2.couleur

    ontLaMemeCouleur = staticmethod(ontLaMemeCouleur)

    # Retourne la carte avec la plus haute valeur
    # None en cas d'égalité
    def plusHauteValeur(c1, c2):
        if(c1.valeur > c2.valeur):
            return c1
        elif(c1.valeur < c2.valeur):
            return c2
        else:
            None

    plusHauteValeur = staticmethod(plusHauteValeur)

    @staticmethod
    def createCardFromStrings(couleur, valeur):
        return Carte(CouleurCarte[couleur], ValeurCarte[valeur])

    # Surcharge de l'opérateur ">"
    def __gt__(self, other):
        return self.valeur > other.valeur

    # Surcharge de l'opérateur ">="
    def __ge__(self, other):
        return self.valeur >= other.valeur

    # Surcharge de l'opérateur "=="
    def isMemeValeur(self, other):
        return self.valeur == other.valeur

    # Getter pour la valeur de la carte
    def getValeur(self):
        return self.valeur

    # Getter pour la couleur de la carte
    def getCouleur(self):
        return self.couleur

    def getNomCarteFormatFichier(self):
        if (self.valeur.value > 10):
            return (str(self.valeur.name).lower() + '_' + str(self.couleur.name).lower())
        else:
            return (str(self.valeur.value).lower() + '_' + str(self.couleur.name).lower())
