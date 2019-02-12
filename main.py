from classes.couleurCarte import *
from classes.valeurCarte import *
from classes.carte import *
from classes.joueur import *
from classes.game import *

j1 = Joueur("j1")
j2 = Joueur("j2")
j3 = Joueur("j3")

g = Game()

g.addJoueur(j1)
g.addJoueur(j2)
g.addJoueur(j3)

print("Nombre de joueurs : " + str(len(g.listeJoueurs)))

print("----------------------------------")

print("Liste des joueurs :")
g.printListeJoueurs()

j1.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.VALET))
j2.addCarte(Carte(CouleurCarte.CARREAU, ValeurCarte.VALET))
j3.addCarte(Carte(CouleurCarte.TREFLE, ValeurCarte.VALET))

g.jouerTour()

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
