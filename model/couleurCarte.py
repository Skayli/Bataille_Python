from enum import Enum

class CouleurCarte(Enum):
    PIQUE = 1
    TREFLE = 2
    COEUR = 3
    CARREAU = 4

    def __str__(self):
        return str(self.name)

    # Surcharge de l'opérateur "=="
    def __eq__(self, other):
        return self.value == other.value
