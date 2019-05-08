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

    def handleNormalTurn(self):
        listeJoueurs = self.getActors()

        # Detection meilleurCarte
        bestCard = listeJoueurs[0].getCarteAJouer()
        for joueur in listeJoueurs:
            if joueur.getCarteAJouer().valeur >  bestCard.valeur:
                bestCard = joueur.getCarteAJouer()

        # Detection bataille
        nbPlayerWithBestCard = 0
        for joueur in listeJoueurs:
            if joueur.getCarteAJouer().valeur == bestCard.valeur:
                nbPlayerWithBestCard += 1

        if nbPlayerWithBestCard == 1: # Pas de bataille
            # Trouver le gagnant
            gagnant = listeJoueurs[0]

            for j in listeJoueurs:
                if j.getCarteAJouer() > gagnant.getCarteAJouer():
                    gagnant = j

            # On met les cartes jouées dans le pli
            for j in listeJoueurs:
                self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(j)
                self.game.pli.append(j.listeCartes.pop(0))

            print("==> GAGNANT SEUL : " + str(gagnant))

            # Passage à l'état suivant
            self.game.stateRamasserPli.setRamasseur(gagnant)
            self.game.adapteur_model.setRamasseur(gagnant)
            self.game.currentState = self.game.stateRamasserPli
            self.game.adapteur_model.setGameStateToRamasserPli()

        else:
            battlePrint = ">>> Bataille entre "

            # Ajout des joueurs participants à la bataille
            self.game.participantsBataille = []

            for j in listeJoueurs:
                if j.getCarteAJouer().valeur == bestCard.valeur:
                    self.game.participantsBataille.append(j)

            print(battlePrint + " et ".join(j.pseudo for j in self.game.participantsBataille) + " <<<")

            # On met les cartes jouées dans le pli
            for j in listeJoueurs:
                self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(j)
                self.game.pli.append(j.listeCartes.pop(0))

            # Check si les joueurs ont assez de cartes
            playersWhoCantBattle = []

            for joueur in self.game.participantsBataille:
                if not self.game.canPlayBattle(joueur):
                    self.game.participantsBataille.remove(joueur)
                    playersWhoCantBattle.append(joueur)

            # GESTION BATAILLE
            if len(self.game.participantsBataille) == 0: # Forcement une partie courte / Fin de la partie
                print("<!> -- BATAILLE IMPOSSIBLE -- <!>")
                print(" et ".join(joueur.pseudo for joueur in playersWhoCantBattle) + " ne peut/peuvent pas se battre")
                self.game.currentState = self.game.stateFinPartie
                self.game.adapteur_model.setGameStateToFinPartie()

            elif len(self.game.participantsBataille) == 1: # Fin de Tour
                print("<!> -- BATAILLE IMPOSSIBLE -- <!>")
                print(" et ".join(joueur.pseudo for joueur in playersWhoCantBattle) + " ne peut/peuvent pas se battre")
                if self.game.retourner == False: # Similaire à au dessus
                    self.game.currentState = self.game.stateFinPartie
                    self.game.adapteur_model.setGameStateToFinPartie()
                else: # Tour final d'une partie retournée finie sur une bataille : le gagnant ramasse les dernieres cartes
                    for player in playersWhoCantBattle: # Poser 1 ou 0 carte
                        if len(player.listeCartes) > 0:
                            self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(player)
                            self.game.pli.append(player.listeCartes.pop(0))

                    self.game.stateRamasserPli.setRamasseur(self.game.participantsBataille[0])
                    self.game.adapteur_model.setRamasseur(self.game.participantsBataille[0])
                    self.game.currentState = self.game.stateRamasserPli
                    self.game.adapteur_model.setGameStateToRamasserPli()

            else: # Bataille possible car il y a au moins 2 joueurs pouvant se battre
                if self.game.retourner == False:
                    self.game.currentState = self.game.stateDeuxiemeCoupBataille
                    self.game.adapteur_model.setGameStateToDeuxiemeCoupBataille()
                else:
                    # Il reste peut etre 1 carte dans la main des joueurs ne pouvant pas jouer : il faut l'ajouter
                    for player in playersWhoCantBattle: # Poser 1 ou 0 carte
                        if len(player.listeCartes) > 0:
                            self.game.adapteur_model.retirerCarteJouerEtAjouterAuPli(player)
                            self.game.pli.append(player.listeCartes.pop(0))

                    # Bataille entre les joueurs restants
                    self.game.currentState = self.game.statePremierCoupBataille
                    self.game.adapteur_model.setGameStateToPremierCoupBataille()

        self.game.startTurn() #Commence le tour suivant
