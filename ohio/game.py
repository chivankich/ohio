from itertools import cycle, chain
from collections import OrderedDict
from deck import Card, Deck


class Game:
    def __init__(self, players):
        self._players = players
        self._score = {player: 0 for player in self._players}
        self._predictions = {player: None for player in self._players}
        self._dealers = cycle(self._players)
        self._last_hand = None

    def create_row(self, dealer):
        dealer_index = self._players.index(dealer)

        return self._players[(dealer_index + 1):] + \
               self._players[:dealer_index + 1]

    def deal_cards(self, dealer, turn, deck):
        if turn > 13:
            turn = 13

        row = cycle(self.create_row(dealer))
        for single in range(turn * len(self._players)):
            next(row).take_card(deck.draw_top())

    def release_trump(self, deck, number):
        if number >= 13:
            return None

        return deck.draw_top()._suite

    def make_predictions(self, dealer, turn, trump):
        row = self.create_row(dealer)

        for player in row:
            predictions = self._predictions
            self._predictions[player] = \
                player.make_prediction(turn, trump, predictions, row, self._score)

    def clean_hands(self):
        for player in self._players:
            player._hands = 0

    def clean_predictions(self):
        for k, v in self._predictions.items():
            self._predictions[k] = None

    def greatest_on_table(self, cards_on_table, trump):
        return sorted([card for card in cards_on_table
                       if card._suite == trump],
                       key=lambda card: card._value, reverse=True)[0]

    def define_winner(self, cards_on_table, trump):
        if any(card._suite == trump for card in cards_on_table.keys()):
            win_card = self.greatest_on_table(cards_on_table.keys(), trump)
            return cards_on_table[win_card]

        instead_of_trump = list(cards_on_table.keys())[0]._suite
        win_card = self.greatest_on_table(cards_on_table.keys(),
                                          instead_of_trump)

        return cards_on_table[win_card]

    def single_deal(self, row, trump, turn):
        cards_on_table = OrderedDict()

        for player in row:
            card = player.give_card(cards_on_table, trump, turn, row, self._score)
            cards_on_table[card] = player

        winner = self.define_winner(cards_on_table, trump)
        winner._hands += 1
        self._last_hand = winner

    def proceed_round(self, turn, row, trump):
        if turn > 13:
            turn = 13

        for single in range(turn):
            self.single_deal(row, trump, turn)
            row = self.create_row(self._last_hand)
            row = row[-1:] + row[:-1]

    def calculate_points(self, player, trump):
        if player._hands == self._predictions[player] == 0 and not trump:
            self._score[player] += 50
        elif player._hands == self._predictions[player] and not trump:
            self._score[player] += player._hands ** 2 + 10

        if player._hands == self._predictions[player] and trump:
            self._score[player] += player._hands ** 2 + 10

    def update_points(self, trump):
        for player in self._players:
            self.calculate_points(player, trump)

    def close_round(self):
        self.clean_hands()
        self.clean_predictions()
        self._last_hand = None

    def single_round(self, number):
        dealer = next(self._dealers)
        self.clean_hands()
        deck = Deck()
        self.deal_cards(dealer, number, deck)
        trump = self.release_trump(deck, number)
        self.make_predictions(dealer, number, trump)
        row = self.create_row(dealer)
        self.proceed_round(number, row, trump)
        self.update_points(trump)
        self.close_round()

    def start(self):
        for turn in range(1, 17):
            self.single_round(turn)
