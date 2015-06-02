from random import shuffle
from card import Card


RANKS = [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8),
         ('9', 9), ('10', 10), ('J', 12), ('Q', 13), ('K', 14), ('A', 15)]
SUITES = ['Spades', 'Hearts', 'Clubs', 'Diamonds']


class Deck:
    def __init__(self):
        self._deck = [Card(suite, rank[0], rank[1])
                      for rank in RANKS for suite in SUITES]
        shuffle(self._deck)
