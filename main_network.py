import getopt
import os
import signal
import sys
import time

from ivy.std_api import *
from ivy.ivy import ivylogger
from ivy.ivy import IvyServer
import logging

from model.couleurCarte import *
from model.valeurCarte import *
from model.carte import *
from model.joueur import *
from model.game import *
from model.adapteur_model import *

ivylogger.setLevel(logging.WARN)

# Ivy functions -------------------------------------------------------------------
def info(fmt, *arg):
        print(fmt % arg)

def on_connection_change(agent, event):
    if event == IvyApplicationDisconnected:
        info('Ivy application %r has disconnected', agent)
    else:
        info("Connexion de %r", agent)
        count = len(IvyGetApplicationList())
        print("Count : " + str(count))
        # count, c'est le nb de bots + le nb de joueur
        if count > 3:
            IvySendDirectMsg(agent, 0, "La partie ne peut plus accueillir de nouveaux joueurs")
            IvySendDieMsg(agent)

    print("---------------------------------------------------------------")

def on_die(agent, _id):
    info('Received the order to die from %r with id = %d', agent, _id)
    global on_die_accepted
    on_die_accepted = True
    # will interrupt the raw_input()/input() in the main loop, below
    os.kill(os.getpid(), signal.SIGINT)

def on_msg(agent, *arg):
    if(adapteur_model.isCommand(arg[0])):
        adapteur_model.analyseCommand(arg[0])
    else:
        print(arg[0])

def on_direct_msg(agent, num_id, msg):
    print("Message de la part de " + IvygetApplcationName(agent) + " : " + msg)

# ------------------------------------------------------------------- Ivy functions
IVYAPPNAME = input("Choisissez votre nom : ") #Nom du joueur
readymsg = None
isHost = False
nbBots = 0
shortGame = False
retourner = True
game = Game(IVYAPPNAME, 'test')
adapteur_model = Adapteur_model()
game.setAdapteurModel(adapteur_model)


while True:
    host = input("Voulez-vous héberger(h) ou rejoindre(r) une partie ? ")
    if host == "h" or host == "r":
        break

if host == "h":
    ivy_bus = "127.255.255.255"
    isHost = True

    while True:
        nbBots = input("Saisissez le nombre de bots à ajouter (3 maximum) : ")
        try:
            nbBots = int(nbBots)
            if (nbBots >=0) and (nbBots <= 3):
                break
        except ValueError:
            pass

    while True:
        isShort = input("Voulez-vous jouer une partie longue(l) ou courte(c) ? ")
        if isShort == "c":
            isShort = True
            break
        elif isShort == "l":
            isShort = False
            break

    while True:
        retourner = input("Voulez-vous jouer la partie classique(c) ou sans carte retournée(r) ? ")
        if retourner == "c":
            retourner = True
            break
        elif retourner == "r":
            retourner = False
            break

else:
    ivy_bus = input("Saissisez l'adresse IP de l'hote de la partie : ")

ivy_bus = ivy_bus+":2010"

IvyInit(IVYAPPNAME, readymsg, 0, on_connection_change, on_die)
IvyStart(ivy_bus)
IvyBindMsg(on_msg, "(.*)")
IvyBindDirectMsg(on_direct_msg)

print("---------------------------------------------------------------")

time.sleep(0.5)
count = len(IvyGetApplicationList())
info("Nombre d'autres utilisateurs connectés : " + str(count))
print("---------------------------------------------------------------")

while 1:
    msg = input('')

    if msg == ".lancer":
        if isHost:
            game.initialiser(nbBots, isShort, retourner)
            game.startTurn()

    elif msg == ".liste":
        print("Liste des joueurs de la partie :")
        game.printListeJoueurs()
    elif msg == ".quit":
        IvyStop()
        break
    elif msg== ".carte":
        for joueur in game.listeJoueurs:
            print("Prochaine carte à jouer de " + joueur.pseudo + " : " + str(joueur.getCarteAJouer()))
    elif msg == ".jouer":
        if (game.started == True) and game.currentState != game.stateRamasserPli:
            if game.participantsTour[0].pseudo == game.name:
                if isHost == True:
                    game.adapteur_model.notifyCurrentPlayerPlayed()
                else:
                    game.adapteur_model.askToHostToNotifyCurrentPlayerPlayed()
            else:
                print("ATTENTION : c'est à " + game.participantsTour[0].pseudo + " de jouer")
        else:
            if not game.started:
                print("Veuillez attendre que la game commence")
            else:
                print("Attendez que " + game.currentState.ramasseur.pseudo + " ramasse les cartes")
    elif msg == ".ramasser":
        if (game.started == True) and game.currentState == game.stateRamasserPli:
            if(game.currentState.ramasseur.pseudo == game.name):
                if isHost == True:
                    game.adapteur_model.notifyCarteRamassee(game.pli[0])
                else:
                    game.adapteur_model.askToHostToNotifyCarteRamassee(game.pli[0])
            else:
                if not game.started:
                    print("Veuillez attendre que la game commence")
                else:
                    print("Il faut finir le tour avant de ramasser")
    elif msg == ".participants":
        print(game.participantsTour)
    else:
        IvySendMsg(IVYAPPNAME + " : " + msg)
