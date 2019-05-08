from model.states.gameState import *
from model.bot import *
import time

class StateDeuxiemeCoupBataille(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("** DEUXIEME TOUR BATAILLE **")
        self.game.participantsTour = self.game.participantsBataille[:]
        super(StateDeuxiemeCoupBataille, self).setPlayerTurnOrder()
        if isinstance(self.game.participantsTour[0], Bot):
            # time.sleep(self.game.botWaitTime)
            nomJoueur = self.game.participantsTour[0].getPseudo()
            carteAJouer = self.game.participantsTour[0].getCarteAJouer()
            action = 'jouer'
            self.game.controller.stockerInfosBots(action, nomJoueur, carteAJouer)
            self.game.adapteur_model.notifyCurrentPlayerPlayed()

    def getActors(self):
        return self.game.participantsBataille

    def actionsTerminees(self):
        return len(self.game.participantsTour) == 0

    def handleTurn(self):
        super(StateDeuxiemeCoupBataille, self).handleNormalTurn()

    def printStateName(self):
        print("StateDeuxiemeCoupBataille")
