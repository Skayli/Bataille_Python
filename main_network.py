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

ivylogger.setLevel(logging.WARN)

IVYAPPNAME = "" # Nom du joueur local
readymsg = None
isFirst = False # Indique si c'est l'initiateur de la partie

def info(fmt, *arg):
        print(fmt % arg)

def on_connection_change(agent, event):
    if event == IvyApplicationDisconnected:
        info('Ivy application %r has disconnected', agent)
    else:
        info("Connexion de %r", agent)
        if isFirst:
            newPlayerName = IvyGetApplicationName(agent)
            joueur = Joueur(newPlayerName)
            game.addJoueur(joueur)
            print("AJout de " + newPlayerName + " à la partie")


def on_die(agent, _id):
    info('Received the order to die from %r with id = %d', agent, _id)
    global on_die_accepted
    on_die_accepted = True
    # will interrupt the raw_input()/input() in the main loop, below
    os.kill(os.getpid(), signal.SIGINT)

def on_msg(agent, *arg):
    info(arg[0])
    # print("From ", agent, " : ", arg[0])


def on_direct_msg(agent, num_id, msg):
    info('%r sent a direct message, id=%s, message=%s', agent, num_id, msg)

IVYAPPNAME = input("Choisissez votre nom : ")

IvyInit(IVYAPPNAME, readymsg, 0, on_connection_change, on_die)
IvyStart("127.255.255.255:2010")
IvyBindMsg(on_msg, "(.*)")

time.sleep(0.5)
info('Go ahead! (type .help for help on commands)')
count = len(IvyGetApplicationList())
print(count)
info("Nombre d'autres utilisateurs connectés : " + str(count))

if count == 0:
    isFirst = True
    joueur = Joueur(IVYAPPNAME)
    game = Game()
    game.addJoueur(joueur)


print("---------------------------------------------------------------")
while 1:
    msg = input('')
    IvySendMsg(IVYAPPNAME + " : " + msg)
