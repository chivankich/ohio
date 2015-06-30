from player import Player
from ui import CLI


class RealPlayer(Player):
    def __init__(self, name):
        super(RealPlayer, self).__init__(name)
        self._prediction = None

    def prediction_without_limit(self, turn, trump, predictions, row, score):
        CLI.overview(turn, trump, predictions, row, score, self._cards)

        print('How many hands you think you will make, ' + self._name + '?')
        hands = input('==> ')
        while not CLI.is_number(hands):
            CLI.overview(turn, trump, predictions, row, score, self._cards)
            print('Please, enter a number,' + self._name + '!')
            hands = input('==> ')
        self._prediction = int(hands)
        return int(hands)

    def verify_prediction(self, hands, limit, turn, trump, predictions, row,
                          score):
        while hands == limit or not CLI.is_number(hands):
            CLI.overview(turn, trump, predictions, row, score, self._cards)
            print('You are the last, '+ self._name + ', \
                  select number, different from ', limit, ': ')
            hands = input('==> ')

        self._prediction = int(hands)
        return int(hands)

    def prediction_with_limit(self, turn, trump, predictions, row, score):
        all_hands = sum([value for value in predictions.values()
                         if value != None])

        if all_hands > turn:
            limit = -1
        else:
            limit = turn - all_hands

        if limit == -1:
            return self.prediction_without_limit(turn, trump, predictions,
                                                 row, score)

        CLI.overview(turn, trump, predictions, row, score, self._cards)
        hands = input('==> ')
        while not CLI.is_number(hands):
            CLI.overview(turn, trump, predictions, row, score, self._cards)
            print('Please, enter a number, ' + self._name + '!')
            hands = input('==> ')
        return self.verify_prediction(int(hands), limit, turn, trump,
                                      predictions, row, score)

    def make_prediction(self, turn, trump, predictions, row, score):
        if turn > 4 and self == row[-1]:
            return self.prediction_with_limit(turn, trump, predictions, row,
                                              score)

        return self.prediction_without_limit(turn, trump, predictions, row,
                                             score)

    def parse_input(self, card):
        if not card:
            return ['error', 'error']

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

    def verify_choice(self, card, cards_on_table, trump, turn, row, score):
        rank, suite = self.parse_input(card)

        while not self.is_card(rank, suite):
            CLI.situation(cards_on_table, trump, turn, row, score,
                          self._cards)
            print('Please, select a card, ' + self._name + ': ')
            selected_card = input('==> ')
            return self.verify_choice(selected_card, cards_on_table, trump,
                                      turn, row, score)

        while not self.is_card_from_hand(rank, suite):
            CLI.situation(cards_on_table, trump, turn, row, score,
                          self._cards)
            print('Please, select a card from your hand, ' + \
                  self._name + ': ')
            selected_card = input('==> ')
            return self.verify_choice(selected_card, cards_on_table, trump,
                                      turn, row, score)

        while not self.is_right_suite(suite, cards_on_table):
            CLI.situation(cards_on_table, trump, turn, row, score,
                          self._cards)
            print('Please, select a card with proper suite, ' + \
                  self._name + ': ')
            selected_card = input('==> ')
            return self.verify_choice(selected_card, cards_on_table, trump,
                                      turn, row, score)

        return self.the_card(rank, suite)

    def give_card(self, cards_on_table, trump, turn, row, score):
        CLI.situation(cards_on_table, trump, turn, row, score, self._cards)

        print('Please, select a card to give, ' + self._name + ': ')
        selected_card = input('==> ')
        card = self.verify_choice(selected_card, cards_on_table, trump, turn,
                                  row, score)

        self._cards.remove(card)
        return card
