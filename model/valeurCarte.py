from enum import Enum

class ValeurCarte(Enum):

    DEUX = 2
    TROIS = 3
    QUATRE = 4
    CINQ = 5
    SIX = 6
    SEPT = 7
    HUIT = 8
    NEUF = 9
    DIX = 10
    VALET = 11
    DAME = 12
    ROI = 13
    AS = 14

    def __str__(self):
        return str(self.name)

    def __gt__(self, other):
        return self.value > other.value

    # Surcharge de l'opérateur ">="
    def __ge__(self, other):
        return self.value >= other.value

    # Surcharge de l'opérateur "=="
    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value
