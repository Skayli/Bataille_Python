class Joueur:

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.listeCartes = []
        self.listeScore = []
        self.initialiser()

    def __repr__(self):
        return "[Joueur => pseudo : " + self.pseudo + " | Nombre de cartes : " + str(self.getNbCartes()) +" | Score Court : " + str(len(self.listeScore)) + "]"

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
        self.listeScore = []

    def addCarte(self, carte):
        self.listeCartes.append(carte)

    def addCarteToScore(self, carte):
        self.listeScore.append(carte)

    def getJoueurInfos(self):
        return "{0} : Nombre de cartes restantes {1}".format(self.pseudo, self.getNbCartes())

    def getVictoireInfos(self):
        return "{0} : Nombre de cartes gagnées = {1}".format(self.pseudo, self.getNbCartes())
