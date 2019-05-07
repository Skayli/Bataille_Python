from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from PIL import Image,ImageTk
from vue.utilitaire import *
from vue.screen import *
from controller.controller import *

class RejoindreScreen(Frame):
    """
    Classe RejoindreScreen
    """
    def __init__(self, parent, mainFrame):
        Frame.__init__(self, parent)
        self.mainFrame = mainFrame
        self.config(bg='linen')
        # Titre du Frame
        self._label = Label(self, text="Lobby Rejoindre Partie", font=mainFrame.title_font, bg='linen', borderwidth=2, relief="groove")
        # Label joueur host
        self._label_host = Label(self, bg='linen')
        # Label pret
        self._label_pret = Label(self, text="Vous êtes prêt !", bg='linen')
        # La zone de saisie pour l'adresse
        self._labelAdresse = Label(self, text="Veuillez renseigner l'adresse de l'hébergeur", font=mainFrame.title_font, bg='linen')
        helv16 = Font(family='Helvetica', size=16, weight='bold')
        self._inputAdresse = Entry(self, font=helv16)
        self._inputAdresse.insert(0, "192.168.1.31")
        # Les boutons
        # self._boutonJouer = Button(self, text='Jouer')
        self._boutonRetour = Button(self, text='Retour', bg='lightcyan2')
        # bouton spécial qui va pop une fois qu'on a trouvé un host
        self._boutonPret = Button(self, text='Prêt', bg='lightcyan2')
        # Polices pour les composants
        helv20 = Font(family='Helvetica', size=20, weight='bold')
        # self._boutonJouer.configure(font = helv20)
        self._boutonRetour.configure(font = helv20)
        self._boutonPret.configure(font = helv20)
        self._label_host.configure(font = helv20)
        self._label_pret.configure(font = helv20)
        # Placement des composants
        self._label.pack(side="top", fill="x", pady=10, ipady=20)
        self._labelAdresse.pack(side="top", fill="x", pady=10)
        self._inputAdresse.pack(side="top", pady=10)
        self._label_host.pack(side="top", fill="x", pady=30)
        self.montrerBoutonPret()
        self.montrerLabelPret()

        # self._boutonJouer.place(relx=0.25, rely=0.90, anchor=SW)
        self._boutonRetour.place(relx=0.75, rely=0.90, anchor=SE)

        self.cacherBoutonPret()
        self.cacherLabelPret()

    def getBoutonJouer(self):
        return self._boutonJouer

    def getBoutonRetour(self):
        return self._boutonRetour

    def getInputAdresse(self):
        return self._inputAdresse

    def getInputAdresseText(self):
        return self._inputAdresse.get().strip()

    def getLabelHost(self):
        return self._label_host

    def setLabelHostText(self, msg):
        self._label_host.configure(text=msg)

    def getBoutonPret(self):
        return self._boutonPret

    def activerBoutonpret(self):
        self._boutonPret.config(state='normal')

    def desactiverBoutonPret(self):
        self._boutonPret.config(state='disabled')

    def montrerBoutonPret(self):
        self._boutonPret.pack(side="top", pady=20)

    def cacherBoutonPret(self):
        self._boutonPret.pack_forget()

    def getLabelPret(self):
        return self._label_pret

    def montrerLabelPret(self):
        self._label_pret.pack(side="top", pady=20)

    def cacherLabelPret(self):
        self._label_pret.pack_forget()

    def actionRetour(self):
        self.mainFrame.show_frame("GameModeScreen")

    def setController(self, controller):
        self._controller = controller
