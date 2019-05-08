from model.states.gameState import *
from model.bot import *
import time

class StateTourNormal(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("** DEBUT DU TOUR **")
        self.game.participantsTour = self.getActors() #reset de la liste des participants au tour
        super(StateTourNormal, self).setPlayerTurnOrder()
        if isinstance(self.game.participantsTour[0], Bot):
            # time.sleep(self.game.botWaitTime)
            nomJoueur = self.game.participantsTour[0].getPseudo()
            carteAJouer = self.game.participantsTour[0].getCarteAJouer()
            action = 'jouer'
            self.game.controller.stockerInfosBots(action, nomJoueur, carteAJouer)
            self.game.adapteur_model.notifyCurrentPlayerPlayed()

    def getActors(self):
        listeActors = []
        for joueur in self.game.listeJoueurs:
            if not self.game.isOver(joueur):
                listeActors.append(joueur)
        return listeActors

    def actionsTerminees(self):
        return len(self.game.participantsTour) == 0

    def handleTurn(self):
        super(StateTourNormal, self).handleNormalTurn()

    def printStateName(self):
        print("StateTourNormal")
