from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from model.game import *
from vue.cadre import *
from vue.screen import *
from vue.screenManager import *
from vue.gameScreen import *
from vue.menuScreen import *
from controller.controller import *
from vue.utilitaire import *

j1 = Joueur("j1")
j2 = Joueur("j2")

g = Game()

g.addJoueur(j1)
g.addJoueur(j2)

g.distribuerCartes()

print("Nombre de joueurs : " + str(len(g.listeJoueurs)))

print("---------------------------------")

print("Liste des joueurs :")
g.printListeJoueurs()

j1.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.ROI))
j1.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.ROI))
j1.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.DEUX))

j2.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.TROIS))

# Partie graphique

root = Tk()

# screenManager = ScreenManager()
cadre = Cadre(root, 900, 900, 'yellow')
# cadre = Cadre(screenManager, 800, 600)

gameScreen = GameScreen(cadre, 600, 600, 'green')
menuScreen = MenuScreen(cadre, 600, 600)
cadre.getScreenManager().ajouterScreen(gameScreen.getType(), gameScreen)
cadre.getScreenManager().ajouterScreen(menuScreen.getType(), menuScreen)

cadre.getScreenManager().setScreenCourant(menuScreen.getType())

controller = Controller(cadre, g)

# cadre.affiche()

x = 0.25
while True:
    menuScreen.getBoutonJouer().place(relx=x, rely=0.80)
    # menuScreen.update()
    cadre.affiche()
    x += 0.1
    print(x)
