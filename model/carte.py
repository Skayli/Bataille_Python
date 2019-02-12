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

    # Surcharge de l'opérateur ">"
    def __gt__(self, other):
        return self.valeur > other.valeur

    # Surcharge de l'opérateur ">="
    def __ge__(self, other):
        return self.valeur >= other.valeur

    # Surcharge de l'opérateur "=="
    def isMemeValeur(self, other):
        return self.valeur == other.valeur
