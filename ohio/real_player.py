import os
from player import Player


class RealPlayer(Player):
    def _init__(self, name):
        super(AIPlayer, self).__init__(name)
        self._prediction = None

    def is_number(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def overview(self, turn, trump, predictions, row):
        os.system('cls')
        print('Round: ', str(turn))
        print()
        print('Predictions:'.center(85))
        print('-' * 85)
        print('|', end='')
        for player in row:
            print(player._name.center(20) + '|', end='')
        print()
        print('-' * 85)
        print('|', end='')
        for player in row:
            if predictions[player] != None:
                print((str(predictions[player]) + ' hands').center(20) + '|', end='')
            else:
                print('thinking...'.center(20) + '|', end='')
        print()
        print('-' * 85)
        print()
        print('Your cards:'.center(12), 'Trump:'.center(12), sep=' ' * 10)
        print('-' * 12 + ' ' * 10 + '-' * 12)
        print(str(self._cards[0]).center(12) + '|', '|' + trump.center(12) + '|', sep=' ' * 8)
        print('-' * 12, '-' * 12, sep=' ' * 10)
        for card in self._cards[1:]:
            print(str(card).center(12) + '|')
            print('-' * 12)
        print()

    def prediction_without_limit(self, turn, trump, predictions, row):
        self.overview(turn, trump, predictions, row)

        print("How many hands you think you will make?")
        hands = input('==> ')
        while not self.is_number(hands):
            self.overview(turn, trump, predictions, row)
            print('Please, enter a number!')
            hands = input('==> ')
        self._prediction = int(hands)
        return int(hands)

    def verify_prediction(self, hands, limit, turn, trump, predictions, row):
        while hands == limit or not self.is_number(hands):
            self.overview(turn, trump, predictions, row)
            print("You are the last, select number, different from ", limit, ": ")
            hands = input('==> ')

        self._prediction = int(hands)
        return int(hands)

    def prediction_with_limit(self, turn, trump, predictions, row):
        all_hands = sum(predictions.values())

        if all_hands > turn:
            limit = -1
        else:
            limit = turn - all_hands

        if limit == -1:
            return self.prediction_without_limit(turn, trump, predictions, row)

        self.overview(turn, trump, predictions, row)
        hands = input('==> ')
        while not self.is_number(hands):
            self.overview(turn, trump, predictions, row)
            print('Please, enter a number!')
            hands = input('==> ')
        return self.verify_prediction(int(hands), limit, turn, trump, predictions, row)

    def make_prediction(self, turn, trump, predictions, row):
        if turn > 4 and self == row[-1]:
            return self.prediction_with_limit(turn, trump, predictions, row)

        return self.prediction_without_limit(turn, trump, predictions, row)

    def situation(self, cards_on_table, trump, turn, row):
        os.system('cls')
        print('Round: ', str(turn))
        print()
        print('Cards on the table:'.center(85))
        print('-' * 85)
        print('|', end='')
        for player in row:
            print((player._name + ' (' + str(player._hands) + '/' + str(player._prediction) +')').center(20) + '|', end='')
        print()
        print('-' * 85)
        print('|', end='')
        for card in list(cards_on_table.keys()):
            print(card)
        print("Your cards: ")
        for card in self._cards:
            print(card)
        print("trump: ", trump)

    def parse_input(self, card):
        if card[0] == '1':
            return [card[:2], card[2:]]

        return [card[0], card[1:]]

    def is_card(self, rank, suite):
        ranks = ['2', '3', '4', '5', '6', '7', '8',
                 '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']

        if not (rank in ranks and suite in suits):
            return False

        return True

    def is_card_from_hand(self, rank, suite):
        if any([card._suite, card._rank] == [suite, rank]
                for card in self._cards):
            return True

        return False

    def is_right_suite(self, card_suite, cards_on_table):
        cards = list(cards_on_table.keys())

        if cards:
            the_suite = cards[0]._suite
        else:
            the_suite = None

        has_such_suite = any(card._suite == the_suite for card in self._cards)

        if has_such_suite and card_suite != the_suite:
            return False

        return True

    def the_card(self, rank, suite):
        return [card for card in self._cards
                if rank == card._rank and suite == card._suite][0]

    def verify_choice(self, card, cards_on_table, trump):
        rank, suite = self.parse_input(card)

        while not self.is_card(rank, suite):
            selected_card = input("Please, select a card: ")
            return self.verify_choice(selected_card, cards_on_table, trump)

        while not self.is_card_from_hand(rank, suite):
            selected_card = input("Please, select a card from your hand: ")
            return self.verify_choice(selected_card, cards_on_table, trump)

        while not self.is_right_suite(suite, cards_on_table):
            selected_card = input("Please, select a card with proper suite: ")
            return self.verify_choice(selected_card, cards_on_table, trump)

        return self.the_card(rank, suite)

    def give_card(self, cards_on_table, trump, turn, row):
        self.situation(cards_on_table, trump, turn, row)

        selected_card = input("Please, select a card to give: ")
        card = self.verify_choice(selected_card, cards_on_table, trump)

        self._cards.remove(card)
        return card
