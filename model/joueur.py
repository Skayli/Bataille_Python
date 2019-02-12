class Joueur:

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.listeCartes = []
        self.initialiser()

    def __repr__(self):
        return "[Joueur => pseudo : " + self.pseudo + " | Nombre de cartes : " + str(self.getNbCartes()) + "]"

    def printListeCartes(self):
        print("\n".join(str(e) for e in self.listeCartes))

    def getNbCartes(self):
        return len(self.listeCartes)

    def getPseudo(self):
        return self.pseudo

    def getCarteAJouer(self):
        return self.listeCartes[0]

    # Initialise un joueur aux valeur de départ
    # Vide la liste des cartes
    def initialiser(self):
        self.listeCartes = []

    def addCarte(self, carte):
        if(carte not in self.listeCartes):
            self.listeCartes.append(carte)
