from abc import abstractmethod

class GameState:

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def initialiser(self):
        pass

    @abstractmethod
    def actionsTerminees(self):
        pass

    @abstractmethod
    def handleTurn(self):
        pass

    @abstractmethod
    def printStateName(self):
        pass

    def setPlayerTurnOrder(self):
        self.game.adapteur_model.setPlayerTurnOrder()
