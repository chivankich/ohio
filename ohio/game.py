from itertools import cycle, chain
from deck import Card, Deck
from player import Player


class Game:
    def __init__(self, players):
        self._players = players
        self._score = {player: 0 for player in self._players}
        self._predictions = {player: None for player in self._players}
        self._dealers = cycle(self._players)

    def create_row(self, dealer):
        dealer_index = self._players.index(dealer)
        return self._players[(dealer_index + 1):] + \
               self._players[:dealer_index + 1]

    def deal_cards(self, dealer, turn, deck):
        row = cycle(self.create_row(dealer))
        for single in range(turn * len(self._players)):
            next(row).take_card(deck.draw_top())

    def make_predictions(self, dealer, turn, koz):
        row = self.create_row(dealer)
        for player in row:
            self._predictions[player] = player.make_prediction(turn, koz)

    def _greatest_on_table(self):
        pass

    def define_winner(self, cards_on_table, koz):
        pass

    def single_deal(self, row, koz):
        cards_on_table = {}
        for player in row:
            card = player.give_card(cards_on_table, koz)
            cards_on_table[player] = card
        winner = self.define_winner(cards_on_table, koz)


    def round(self, number):
        dealer = next(self._dealers)
        # print('Logger: ', 'dealer - ', dealer)
        deck = Deck()
        # print(deck._deck)
        self.deal_cards(dealer, number, deck)
        koz = deck.draw_top()._suite
        # print('Logger: ', 'koz - ', koz)
        # print('Logger: Deck after dealing - ', deck._deck)
        self.make_predictions(dealer, turn)
        winner = self.create_row(dealer)[0]
        for single in range(number):
            self._single_deal()
