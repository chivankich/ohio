from random import randint, choice
from player import Player
from deck import SUITES


class AIPlayer(Player):
    def _init__(self, name):
        super(AIPlayer, self).__init__(name)
        self._prediction = None

    def cards_by_suite(self, suite):
        return sorted([card for card in self._cards if card._suite == suite],
                       key=lambda card: card._value,
                       reverse=True)

    def higher_cards_than(self, suite, value):
        cards = self.cards_by_suite(suite)
        return [card for card in cards if card._value >= value]

    def lower_cards_than(self, suite, value):
        cards = self.cards_by_suite(suite)
        return [card for card in cards if card._value <= value]

    def points_from_aces(self):
        return len([card for card in self._cards if card._value == 15])

    def is_covered(self, card):
        from_same_suite = self.cards_by_suite(card._suite)
        enough_cards = 15 - card._value
        return len(from_same_suite) - 1 - enough_cards >= 0

    def points_from_covered_cards(self):
        hands = 0
        for suite in SUITES:
            quite_high_cards = self.higher_cards_than(suite, 10)
            for card in quite_high_cards:
                if self.is_covered(card):
                    hands += 1
        return hands

    def points_from_low_kozes(self, turn, koz):
        if not koz:
            return 0
        low_kozes = len(self.lower_cards_than(koz, 9))
        if turn / 2 < low_kozes:
            feel_unlucky = randint(0, 1)
            return low_kozes - feel_unlucky
        if low_kozes:
            return randint(0, low_kozes)
        return 0

    def has_conflict(self, turn, predictions):
        other_hands = sum([value for value in predictions.values()
                           if value != None])
        return other_hands == turn

    def resolved_conflict(self, hands):
        if not hands:
            self._prediction = 1
            return 1
        hands += choice([1, -1])
        self._prediction = hands
        return hands

    def make_prediction(self, turn, koz, predictions, row):
        predicted_hands = sum([self.points_from_aces(),
                               self.points_from_covered_cards(),
                               self.points_from_low_kozes(turn, koz)])
        if row[-1] == self and self.has_conflict(turn, predictions):
            return self.resolved_conflict(predicted_hands)
        self._prediction = predicted_hands
        return predicted_hands

    def choose_the_best(self, greatest):
        card = sorted(self._cards,
                      key=lambda card: card._value,
                      reverse=greatest)[0]
        self._cards.remove(card)
        return card

    def choose_from_others(self, card, koz):
        cards = sorted(self._cards,
                       key=lambda card: card._value,
                       reverse=True)
        not_kozes = [card for card in cards if card._suite != koz]
        if not_kozes:
            card = not_kozes[0]
            self._cards.remove(card)
            return card
        card = cards[-1]
        self._cards.remove(card)
        return card

    def choose_highest_under(self, card, koz):
        lower_cards = self.lower_cards_than(card._suite, card._value - 1)
        higher_cards = self.higher_cards_than(card._suite, card._value + 1)
        if lower_cards:
            card = lower_cards[0]
            self._cards.remove(card)
            return card
        if higher_cards:
            card = higher_cards[-1]
            self._cards.remove(card)
            return card
        return self.choose_from_others(card, koz)

    def no_more_hands(self, cards_on_table, koz):
        given_cards = list(cards_on_table.keys())
        if not given_cards:
            return self.choose_the_best(False)
        return self.choose_highest_under(given_cards[0], koz)

    def try_to_get_with_others(self, card, koz):
        cards = sorted(self._cards,
                       key=lambda card: card._value,
                       reverse=True)
        kozes = [card for card in cards if card._suite == koz]
        if kozes:
            card = choice(kozes)
            self._cards.remove(card)
            return card
        card = cards[-1]
        self._cards.remove(card)
        return card

    def try_to_get(self, card, koz):
        lower_cards = self.lower_cards_than(card._suite, card._value - 1)
        higher_cards = self.higher_cards_than(card._suite, card._value + 1)
        if higher_cards:
            card = higher_cards[0]
            self._cards.remove(card)
            return card
        if lower_cards:
            card = lower_cards[-1]
            self._cards.remove(card)
            return card
        return self.try_to_get_with_others(card, koz)

    def need_more_hands(self, cards_on_table, koz):
        given_cards = list(cards_on_table.keys())
        if not given_cards:
            return self.choose_the_best(True)
        return self.try_to_get(given_cards[0], koz)

    def give_card(self, cards_on_table, koz):
        if self._hands == self._prediction:
            return self.no_more_hands(cards_on_table, koz)
        return self.need_more_hands(cards_on_table, koz)
