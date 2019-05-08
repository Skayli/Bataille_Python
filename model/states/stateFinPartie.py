from model.states.gameState import *
import time

class StateFinPartie(GameState):

    def __init__(self, game):
        super().__init__(game)

    def initialiser(self):
        print("[StateFinPartie] Initialisation")
        print("PARTIE TERMINEE")

        if self.game.court == True: # A la fin d'une partie courte, il faut ajouter les cartes du joueur pouvant encore jouer à son score
            for joueur in self.game.listeJoueurs:
                if not self.game.isOver(joueur):
                    self.game.adapteur_model.addPlayerCardToScore(joueur)

        gagnant = self.game.getWinner()

        if len(gagnant) > 1:
            print("EX AEQUO :")
            for j in gagnant:
                print(str(j))
        else:
            print("Gagnant : " + str(gagnant[0]))

        for j in self.game.listeJoueurs:
            print(str(j))

    def getActors(self):
        return self.game.participantsBataille[:]

    def actionsTerminees(self):
        return len(self.game.participantsTour) == 0

    def handleTurn(self):
        print("[StateFinPartie] handleTurn")

    def printStateName(self):
        print("StateFinPartie")
