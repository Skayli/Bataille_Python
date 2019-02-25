# On importe Tkinter
# import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
# from vue.utilitaire import *

class Screen:
    """
    Classe définissant un écran générique avec
    le module Tkinter
    """

    def __init__(self, root, width=600, height=600, bg='white'):
        self._canvas = Canvas(root, width=width, height=height, bg=bg)
        self._parent = root

    def getCanvas(self):
        return self._canvas

    def getParent(self):
        return self._parent

    def affiche(self):
        self._canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def getType(self):
        return str(type(self).__name__)
