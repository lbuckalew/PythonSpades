import math
import random
from enum import Enum
import numpy as np

class CARD_SUITS(Enum):
    CLUB = 1
    DIAMOND = 2
    HEART = 3
    SPADE = 4

class CARD_RANKS(Enum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13

class Card:
    def __init__(self, id):
        self.id = id

        suit = int(math.ceil(id / 13))
        if suit < 0:
            raise ValueError()
        elif (suit >= 1) and (suit <= 4):
            self.suit = CARD_SUITS(suit)
        else:
            raise ValueError()

        rank = (id - ((suit - 1) * 13))
        self.rank = CARD_RANKS(rank)

    def __str__(self):
        shortSuit = self.suit.name[0]
        if self.rank.value <= 9:
            shortRank = self.rank.value + 1
        else:
            shortRank = self.rank.name[0]

        s = "|{}*{}|".format(shortRank, shortSuit)
        return s

class Deck:
    def __init__(self):
        # make random order of cards
        ids = np.linspace(1, 52, 52).tolist()
        self.stack = []
        for i in ids:
            self.stack.append(Card(i))
        self.shuffle()

    def draw(self):
        return self.stack.pop()

    def shuffle(self):
        random.shuffle(self.stack)