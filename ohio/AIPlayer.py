from random import randint, choice
from player import Player


class AIPlayer(Player):
    def make_prediction(self, turn, koz, predictions, row):
        return randint(0, turn)

    def give_card(self, cards_on_table, koz):
        if not cards_on_table:
            card = choice(self._cards)
            self._cards.remove(card)
            return card

        first = list(cards_on_table.keys())[0]

        possible = [card for card in self._cards
                    if card._suite == first._suite]
        if possible:
            card = choice(possible)
            self._cards.remove(card)
            return card

        card = choice(self._cards)
        self._cards.remove(card)
        return card
