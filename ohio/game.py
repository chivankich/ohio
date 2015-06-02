from itertools import cycle, chain
from deck import Card, Deck
from player import Player


class Game:
    def __init__(self, players):
        self._players = players
        self._score = {player: 0 for player in self._players}
        self._predictions = {player: 0 for player in self._players}
        self._dealers = cycle(self._players)

    def _deal_cards(self, dealer, turn, deck):
        dealer_index = self._players.index(dealer)
        row = cycle(chain.from_iterable([self._players[(dealer_index + 1):],
                                         self._players[:dealer_index + 1]]))
        for single in range(turn * len(self._players)):
            next(row).take(deck.draw_top())

    def _make_predictions(self, dealer, turn):
        dealer_index = self._players.index(dealer)
        row = chain.from_iterable([self._players[(dealer_index + 1):],
                                   self._players[:dealer_index + 1]])
        for player in row:
            pass


    def round(self, number):
        dealer = next(self._dealers)
        # print('Logger: ', 'dealer - ', dealer)
        deck = Deck()
        # print(deck._deck)
        self._deal_cards(dealer, number, deck)
        koz = deck.draw_top()._suite
        # print('Logger: ', 'koz - ', koz)
        # print('Logger: Deck after dealing - ', deck._deck)
        self._make_predictions
