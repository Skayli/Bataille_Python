from model.states.gameState import *

class StatePremierCoupBataille(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("[StatePremierCoupBataille] Initialisation")
        self.game.participantsTour = self.game.participantsBataille[:]
        super(StatePremierCoupBataille, self).setPlayerTurnOrder()

    def getActors(self):
        return self.game.participantsBataille[:]

    def actionsTerminees(self):
        return len(self.game.participantsTour) == 0

    def handleTurn(self):
        print("[StatePremierCoupBataille] handleTurn")
        for j in self.game.participantsBataille:
            self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(j)
            self.game.pli.append(j.listeCartes.pop(0))

        self.game.currentState = self.game.stateDeuxiemeCoupBataille
        self.game.adapteur_model.setGameStateToDeuxiemeCoupBataille()
        self.game.startTurn()

    def printStateName(self):
        print("StatePremierCoupBataille")
