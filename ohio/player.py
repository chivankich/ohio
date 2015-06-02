class Player:
    def __init__(self, name):
        self._name = name
        self._cards = []

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def take(self, card):
        self._cards.append(card)
