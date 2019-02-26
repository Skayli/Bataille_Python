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

root = Tk()
root.withdraw()
app = Controller(root);
root.mainloop()
