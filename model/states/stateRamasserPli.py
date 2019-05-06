from model.states.gameState import *

class StateRamasserPli(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("[StateRamasserPli] Initialisation => rien a faire")

    def getActors(self):
        print("[StateRamasserPli] getActors => rien a faire")

    def actionsTerminees(self):
        return len(self.game.pli) == 0

    def handleTurn(self):
        print("[StateRamasserPli] handleTurn | retour debut tour")
        self.game.currentState = self.game.stateTourNormal
        self.game.adapteur_model.setGameStateToTourNormal()
        self.game.startTurn()

    def setRamasseur(self, joueur):
        self.ramasseur = joueur

    def printStateName(self):
        print("StateRamasserPli")
