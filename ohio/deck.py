from random import shuffle


RANKS = [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8),
         ('9', 9), ('10', 10), ('J', 12), ('Q', 13), ('K', 14), ('A', 15)]
SUITES = ['Spades', 'Hearts', 'Clubs', 'Diamonds']


class Card:
    def __init__(self, suite, rank, value):
        self._suite = suite
        self._rank = rank
        self._value = value

    def __repr__(self):
        return self._rank + ' ' + self._suite

    def __str__(self):
        return self._rank + ' ' + self._suite

    def __eq__(self, other):
        return [self._suite, self._value] == [other._suite, other._value]

    def __lt__(self, other):
        return self._value < other._value

    def __hash__(self):
        return hash(self._value)


class Deck:
    def __init__(self):
        self._deck = [Card(suite, rank[0], rank[1])
                      for rank in RANKS for suite in SUITES]
        shuffle(self._deck)

    def __str__(self):
        return str(self._deck)

    def __repr__(self):
        return repr(self._deck)

    def draw_top(self):
        if self._deck:
            return self._deck.pop(-1)

        return None
