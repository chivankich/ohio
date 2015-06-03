from random import randint, choice


class Player:
    def __init__(self, name):
        self._name = name
        self._cards = []
        self._hands = 0

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def take_card(self, card):
        self._cards.append(card)

    def make_prediction(self, turn, koz):
        return randint(0, turn)

    def give_card(self, cards_on_table, koz):
        pass

