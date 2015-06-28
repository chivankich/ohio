from player import Player


class RealPlayer(Player):
    def overview(self, turn, trump, predictions, row):
        in_row = row.index(self)

        for player in row[:in_row]:
            print(player, " said ", predictions[player], " hands")
        print("trump: ", trump)
        print("Your cards: ")
        for card in self._cards:
            print(card)

    def prediction_without_limit(self, turn, trump, predictions, row):
        self.overview(turn, trump, predictions, row)

        hands = input("How many hands you think you will make? ")
        return int(hands)

    def verify_prediction(self, hands, limit):
        while hands == limit:
            hands = input("You are last, select number, different from ",
                          limit, ": ")
            return self.verify_prediction(hands, limit)

        return hands

    def prediction_with_limit(self, turn, trump, predictions, row):
        all_hands = sum(predictions.values())

        if all_hands > turn:
            limit = -1
        else:
            limit = turn - all_hands

        if limit == -1:
            return self.prediction_without_limit(turn, trump, predictions, row)

        self.overview(turn, trump, predictions, row)
        hands = input("How many hands you think you will make? ")
        return self.verify_prediction(hands, limit)

    def make_prediction(self, turn, trump, predictions, row):
        if turn > 4 and self == row[-1]:
            return self.prediction_with_limit(turn, trump, predictions, row)

        return self.prediction_without_limit(turn, trump, predictions, row)

    def situation(self, cards_on_table, trump):
        print("Cards on the table: ")
        for card in list(cards_on_table.keys()):
            print(card, " from ", cards_on_table[card]._name)
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

    def give_card(self, cards_on_table, trump):
        self.situation(cards_on_table, trump)

        selected_card = input("Please, select a card to give: ")
        card = self.verify_choice(selected_card, cards_on_table, trump)

        self._cards.remove(card)
        return card
