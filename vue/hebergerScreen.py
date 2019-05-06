from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class HebergerScreen(Frame):
    """
    Classe HebergerScreen
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        # Pour compter le nombre de joueurs humains
        self._nbJoueursHumains = 1
        self._nbJoueursHumainsPrets = 1
        self._nomsJoueurs = []
        # Titre du Frame
        self._label = Label(self, text="Lobby Host", font=mainFrame.title_font)
        # Infos sur les autres joueurs
        self._labelsJoueurs = []
        # ComboBox pour choisir le nombre de joueurs
        self._comboBoxValues = ["Aucun bot", "1 adversaire", "2 adversaires", "3 adversaires"]
        self._comboBoxAdversaires = Combobox(self, values=self._comboBoxValues)
        self._comboBoxAdversaires.current(0)
        self._comboBoxAdversaires.configure(state="readonly")
        self._comboBoxAdversaires.bind("<<ComboboxSelected>>", self.comboBoxChange)
        # Les boutons
        # self._boutonJouer = Button(self, text='Jouer', command= lambda: mainFrame.show_frame("GameScreen"))
        self._boutonJouer = Button(self, text='Jouer')
        self._boutonRetour = Button(self, text='Retour', command= lambda: self.mainFrame.show_frame("GameModeScreen"))
        # Polices pour les composants
        self._helv20 = Font(family='Helvetica', size=20, weight='bold')
        self._boutonJouer.configure(font = self._helv20)
        self._boutonRetour.configure(font = self._helv20)
        # Placement composants
        self._label.pack(side="top", fill="x", pady=10)
        self._comboBoxAdversaires.pack(side="top", pady=30)
        self._boutonJouer.place(relx=0.25, rely=0.90, anchor=SW)
        self._boutonRetour.place(relx=0.75, rely=0.90, anchor=SE)
        # Par défaut désactiver boutonJouer
        self.desactiverBoutonJouer()

    def updateLabelsJoueurs(self):
        # Placement des composants représentant les joueurs qui arrivent sur le lobby
        for i in range(0, (len(self._labelsJoueurs))):
            self._labelsJoueurs[i].pack(side="top", fill="x", pady=10)

    def getLabelsJoueurs(self):
        return self._labelsJoueurs

    def ajouterNomJoueur(self, nom):
        self._nomsJoueurs.append(nom)

    def getNomsJoueurs(self):
        return self._nomsJoueurs

    def getBoutonJouer(self):
        return self._boutonJouer

    def activerBoutonJouer(self):
        self._boutonJouer.config(state='normal')

    def desactiverBoutonJouer(self):
        self._boutonJouer.config(state='disabled')

    def updateEtatBoutonJouer(self):
        if self.isAllJoueursHumainsPrets():
            self.activerBoutonJouer()
        else:
            self.desactiverBoutonJouer()

    def updateComboBoxBots(self):
        newValues = []
        selectedIndex = self._comboBoxAdversaires.current()
        if selectedIndex > (4-self._nbJoueursHumains):
            selectedIndex = (4-self._nbJoueursHumains)
        for i in range((4-self._nbJoueursHumains)+1):
            newValues.append(self._comboBoxValues[i])
        self._comboBoxAdversaires.config(values=newValues)
        self._comboBoxAdversaires.current(selectedIndex)

    def comboBoxChange(self, event):
        if (self._nbJoueursHumains == 1):
            if (self._comboBoxAdversaires.current() > 0):
                self.activerBoutonJouer()
            else:
                self.desactiverBoutonJouer()

    def getBoutonRetour(self):
        return self._boutonRetour

    def getComboBoxNombreAdversaires(self):
        return self._comboBoxAdversaires

    def getSelectedItemComboBoxAdversaires(self):
        return self._comboBoxAdversaires.get()

    def actionRetour(self):
        self.mainFrame.show_frame("GameModeScreen")

    def getNombreJoueursHumains(self):
        return self._nbJoueursHumains

    def incrementerNombreJoueursHumains(self):
        self._nbJoueursHumains += 1

    def decrementerNombreJoueursHumains(self):
        self._nbJoueursHumains -= 1

    def getNombreJoueursHumainsPrets(self):
        return self._nbJoueursHumainsPrets

    def incrementerNombreJoueursHumainsPrets(self):
        self._nbJoueursHumainsPrets += 1

    def decrementerNombreJoueursHumainsPrets(self):
        self._nbJoueursHumainsPrets -= 1

    def isAllJoueursHumainsPrets(self):
        return (self._nbJoueursHumains == self._nbJoueursHumainsPrets)

    def setController(self, controller):
        self._controller = controller
