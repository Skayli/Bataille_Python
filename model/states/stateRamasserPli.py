from model.states.gameState import *
from model.bot import *
import time

class StateRamasserPli(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("[StateRamasserPli] Initialisation => Ramassage en cours par " + self.ramasseur.pseudo)
        if isinstance(self.ramasseur, Bot):
            # time.sleep(self.game.botWaitTime)
            nomJoueur = self.game.currentState.ramasseur.getPseudo()
            carteAJouer = self.game.pli[0]
            action = 'ramasser'
            self.game.controller.stockerInfosBots(action, nomJoueur, carteAJouer)
            self.game.adapteur_model.notifyCarteRamassee(self.game.pli[0])

    def getActors(self):
        print("[StateRamasserPli] getActors => rien a faire")

    def actionsTerminees(self):
        return len(self.game.pli) == 0

    def handleTurn(self):
        if self.game.isFinished():
            print("[StateRamasserPli] Fin de partie")
            self.game.currentState = self.game.stateFinPartie
            self.game.adapteur_model.setGameStateToFinPartie()
        else:
            print("[StateRamasserPli] Retour debut tour")
            self.game.currentState = self.game.stateTourNormal
            self.game.adapteur_model.setGameStateToTourNormal()

        self.game.startTurn()

    def setRamasseur(self, joueur):
        self.ramasseur = joueur

    def printStateName(self):
        print("StateRamasserPli")
