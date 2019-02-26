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

<<<<<<< HEAD
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
#
# j1.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.ROI))
# j1.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.ROI))
# j1.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.DEUX))
#
# j2.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.TROIS))

# Partie graphique

=======
>>>>>>> 29902604a9c76445257d292ad5d6a2117e0a1f65
root = Tk()
root.withdraw()
app = Controller(root);
root.mainloop()
