from model.states.gameState import *

class StateDeuxiemeCoupBataille(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("[StateDeuxiemeCoupBataille] Initialisation")
        self.game.participantsTour = self.game.participantsBataille[:]
        super(StateDeuxiemeCoupBataille, self).setPlayerTurnOrder()

    def getActors(self):
        return self.game.participantsBataille[:]

    def actionsTerminees(self):
        return len(self.game.participantsTour) == 0

    def handleTurn(self):
        print("[StateDeuxiemeCoupBataille] handleTurn")
        listeJoueurs = self.game.participantsBataille

        # Detection bataille
        battleCard = None

        for j1 in listeJoueurs:
            print("Carte " + j1.pseudo + " : " + str(j1.getCarteAJouer()))
            for j2 in listeJoueurs:
                if j1 != j2 and j1.getCarteAJouer().valeur ==  j2.getCarteAJouer().valeur:
                    if battleCard == None or battleCard < j1.getCarteAJouer():
                        battleCard = j1.getCarteAJouer()

        if battleCard == None: # Pas de bataille
            # Trouver le gagnant
            gagnant = listeJoueurs[0]

            for j in listeJoueurs:
                if j.getCarteAJouer() > gagnant.getCarteAJouer():
                    gagnant = j

            for j in listeJoueurs:
                self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(j)
                self.game.pli.append(j.listeCartes.pop(0))

            print("Fin tour normal : ")
            print("GAGNANT SEUL :\n" + str(gagnant))

            # Passage à l'état suivant
            self.game.stateRamasserPli.setRamasseur(gagnant)
            self.game.adapteur_model.setRamasseur(gagnant)
            self.game.currentState = self.game.stateRamasserPli
            self.game.adapteur_model.setGameStateToRamasserPli()

        else:
            print("bataille")
            # Ajout des joueurs participants à la bataille
            self.game.participantsBataille = []

            for j in listeJoueurs:
                if j.getCarteAJouer().valeur == battleCard.valeur:
                    self.game.participantsBataille.append(j)

            # On met les cartes jouées dans le pli
            for j in listeJoueurs:
                self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(j)
                self.game.pli.append(j.listeCartes.pop(0))

            self.game.currentState = self.game.statePremierCoupBataille
            self.game.adapteur_model.setGameStateToPremierCoupBataille()


        self.game.startTurn() #Commence le tour suivant

    def printStateName(self):
        print("StateDeuxiemeCoupBataille")
