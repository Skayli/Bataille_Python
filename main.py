from classes.couleurCarte import *
from classes.valeurCarte import *
from classes.carte import *
from classes.joueur import *
from classes.game import *

j1 = Joueur("j1")
j2 = Joueur("j2")
j3 = Joueur("j3")
j4 = Joueur("j4")

g = Game()

g.addJoueur(j1)
g.addJoueur(j2)
g.addJoueur(j3)
g.addJoueur(j4)

print("Nombre de joueurs : " + str(len(g.listeJoueurs)))

print("---------------------------------")

print("Liste des joueurs :")
g.printListeJoueurs()

j1.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.ROI))
j1.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.ROI))
j1.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.DEUX))

j2.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.TROIS))

j3.addCarte(Carte(CouleurCarte.TREFLE, ValeurCarte.DEUX))

j4.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.ROI))
j4.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.ROI))
j4.addCarte(Carte(CouleurCarte.COEUR, ValeurCarte.AS))

g.jouerTour()


print("----------------------------------")
print("j4 : ")
j4.printListeCartes()

# print("----------------------------------")
#
# g.distribuerCartes()
#
# print("Liste des cartes restantes :")
# g.printListeCartes()
#
# print("----------------------------------")
#
# print("Listes des cartes de chaque joueurs : ")
# g.printListeJoueurs()
#
# print("----------------------------------")
#
# print("Liste des cartes de j1")
# j1.printListeCartes()
#
# print("----------------------------------")
#
# print("Liste des cartes de j2")
# j2.printListeCartes()
#
# print("----------------------------------")
