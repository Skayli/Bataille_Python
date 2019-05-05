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
from vue.adapteur_vue import *

class IvyBus:
    """Classe définissant le bus Ivy
    """

    def __init__(self, pseudo, game, cadre, isHost, adresse):
        ivylogger.setLevel(logging.WARN)
        # ------------------------------------------------------------------- Ivy functions
        IVYAPPNAME = pseudo #Nom du joueur
        readymsg = None
        self._isHost = isHost
        # self._game = Game(IVYAPPNAME)
        self._adapteur_model = Adapteur_model()
        # self._game.setAdapteurModel(self._adapteur_model)

        # self._cadre = cadre
        self._adapteur_vue = Adapteur_vue()
        cadre.setAdapteurVue(self._adapteur_vue)

        ivy_bus = adresse
        # if self._isHost == True:
        #     ivy_bus = "192.168.1.255"
        #     self._isHost = True
        # else:
        #     ivy_bus =  "192.168.1.31"#input("Saissisez l'adresse IP de l'hote de la partie : ")

        ivy_bus = ivy_bus+":2010"

        IvyInit(IVYAPPNAME, readymsg, 0, self.on_connection_change, self.on_die)
        IvyStart(ivy_bus)
        IvyBindMsg(self.on_msg, "(.*)")
        IvyBindDirectMsg(self.on_direct_msg)

        print("---------------------------------------------------------------")

        time.sleep(0.5)
        count = len(IvyGetApplicationList())
        self.info("Nombre d'autres utilisateurs connectés : " + str(count))
        print("---------------------------------------------------------------")

        # while 1:
        #     msg = input('')
        #
        #     if msg == ".lancer":
        #         if self._isHost:
        #             game.initialiser()
        #     elif msg == ".liste":
        #         print("Liste des joueurs de la partie :")
        #         game.printListeJoueurs()
        #     elif msg == ".quit":
        #         IvyStop()
        #         break
        #     elif msg== ".carte":
        #         print("Prochaine carte à jouer de J1 : " + str(game.getPlayerByName("j1").getCarteAJouer()))
        #         print("Prochaine carte à jouer de J2 : " + str(game.getPlayerByName("j2").getCarteAJouer()))
        #     else:
        #         IvySendMsg(IVYAPPNAME + " : " + msg)

    # Ivy functions -------------------------------------------------------------------
    def info(self, fmt, *arg):
            print(fmt % arg)

    def on_connection_change(self, agent, event):
        if event == IvyApplicationDisconnected:
            self.info('Ivy application %r has disconnected', agent)
        else:
            self.info("Connexion de %r", agent)
            count = len(IvyGetApplicationList())
            print("Count : " + str(count))
            # Si on est le host alors on va donner l'ordre de refresh la liste des joueurs dans le lobby du host
            agentName = repr(agent).strip('0123456789.:() ')
            if (self._isHost == True):
                self._adapteur_vue.prepareCommand(("CMDVIEW | updateLabelsJoueursHebergerScreen | %s" % agentName))
            else:
                self._adapteur_vue.prepareCommand(("CMDVIEW | updateLabelHostRejoindreScreen | %s" % agentName))
            if count > 3:
                IvySendDirectMsg(agent, 0, "La partie ne peut plus accueillir de nouveaux joueurs")
                IvySendDieMsg(agent)

        print("---------------------------------------------------------------")

    def on_die(self, agent, _id):
        self.info('Received the order to die from %r with id = %d', agent, _id)
        global on_die_accepted
        on_die_accepted = True
        # will interrupt the raw_input()/input() in the main loop, below
        os.kill(os.getpid(), signal.SIGINT)

    def on_msg(self, agent, *arg):
        if(self._adapteur_model.isCommand(arg[0])):
            self._adapteur_model.analyseCommand(arg[0])
        elif(self._adapteur_vue.isCommand(arg[0])):
            self._adapteur_vue.prepareCommand(arg[0])
        else:
            print(arg[0])

    def on_direct_msg(self, agent, num_id, msg):
        print("Message de la part de " + IvygetApplcationName(agent) + " : " + msg)

    def getAdapteur_model(self):
        return self._adapteur_model

    def getAdapteur_vue(self):
        return self._adapteur_vue