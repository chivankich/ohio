import unittest
from random import randint
from collections import OrderedDict
from deck import Card, Deck
from player import Player
from AIPlayer import AIPlayer
from game import Game


class TestSeparateCards(unittest.TestCase):
    def test_is_equal(self):
        card = Card('Spades', '6', 6)
        other_card = Card('Spades', '6', 6)
        self.assertEqual(card, other_card)

    def test_not_equal(self):
        card = Card('Spades', '6', 6)
        other_card = Card('Spades', '10', 10)
        self.assertNotEqual(card, other_card)

    def test_card_less_than_other(self):
        card = Card('Diamonds', 'J', 12)
        other_card = Card('Diamonds', 'K', 14)
        self.assertTrue(card < other_card)

    def test_card_higher_than_other(self):
        card = Card('Diamonds', 'J', 12)
        other_card = Card('Diamonds', 'K', 14)
        self.assertFalse(card > other_card)


class TestDeck(unittest.TestCase):
    def test_size_deck(self):
        deck = Deck()
        self.assertEqual(len(deck._deck), 52)

    def test_draw_top_card(self):
        deck = Deck()
        top_card = deck._deck[-1]
        self.assertEqual(top_card, deck.draw_top())


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player('Player1')

    def test_initial_cards(self):
        self.assertEqual(self.player._cards, [])

    def test_initial_hands(self):
        self.assertEqual(self.player._hands, 0)

    def test_take_card(self):
        card = Card('Hearts', 'A', 15)
        self.player.take_card(card)
        self.assertEqual(self.player._cards, [card])


class TestGameRules(unittest.TestCase):
    def setUp(self):
        self.player1 = AIPlayer('Player1')
        self.player2 = AIPlayer('Player2')
        self.player3 = AIPlayer('Player3')
        self.player4 = AIPlayer('Player4')
        self.game = Game([self.player1, self.player2,
                          self.player3, self.player4])

    def test_create_row(self):
        dealer = self.player3
        row = [self.player4, self.player1, self.player2, self.player3]
        self .assertEqual(self.game.create_row(self.player3), row)

    def test_deal_cards(self):
        dealer = self.player3
        turn = 1
        deck = Deck()
        last_four = list(reversed(deck._deck[-4:]))
        self.game.deal_cards(dealer, turn, deck)
        player_cards = [self.player4._cards[0], self.player1._cards[0],
                        self.player2._cards[0], self.player3._cards[0]]
        self.assertEqual(player_cards, last_four)

    def test_release_trump(self):
        deck = Deck()
        number = 7
        suite = deck._deck[-1]._suite
        self.assertEqual(self.game.release_trump(deck, number), suite)

    def test_no_trump(self):
        deck = Deck()
        number = 15
        self.assertIsNone(self.game.release_trump(deck, number))

    def test_make_predictions(self):
        deck = Deck()
        dealer = self.player3
        turn = 2
        trump = deck._deck[-9]._suite
        self.game.deal_cards(dealer, turn, deck)
        self.game.make_predictions(dealer, turn, trump)
        predictions = list(self.game._predictions.values())
        none_values = [None, None, None, None]
        self.assertNotEqual(predictions, none_values)

    def test_clean_hands(self):
        players = [self.player1, self.player2, self.player3, self.player4]
        for player in players:
            player._hands = randint(0, 4)
        self.game.clean_hands()
        no_hands = [player._hands for player in players]
        self.assertEqual(no_hands, [0, 0, 0, 0])

    def test_clean_predictions(self):
        deck = Deck()
        dealer = self.player3
        turn = 2
        trump = deck._deck[-9]._suite
        self.game.deal_cards(dealer, turn, deck)
        self.game.make_predictions(dealer, turn, trump)
        self.game.clean_predictions()
        self.assertEqual(list(self.game._predictions.values()), [None, None,
                                                                 None, None])

    def test_gratest_on_table(self):
        seven_diamonds = Card('Diamonds', '7', 7)
        ten_diamonds = Card('Diamonds', '10', 10)
        two_spades = Card('Spades', '2', 2)
        jack_hearts = Card('Hearts', 'J', 12)
        cards_on_table = [seven_diamonds, ten_diamonds,
                          two_spades, jack_hearts]
        trump = 'Diamonds'
        greatest = self.game.greatest_on_table(cards_on_table, trump)
        self.assertEqual(greatest, ten_diamonds)

    def test_define_winner(self):
        seven_diamonds = Card('Diamonds', '7', 7)
        ten_diamonds = Card('Diamonds', '10', 10)
        ace_spades = Card('Spades', 'A', 15)
        jack_hearts = Card('Hearts', 'J', 12)
        cards_on_table = OrderedDict({seven_diamonds: self.player4,
                                      ten_diamonds: self.player1,
                                      ace_spades: self.player2,
                                      jack_hearts: self.player3})
        trump = 'Clubs'
        winner = self.game.define_winner(cards_on_table, trump)
        self.assertEqual(winner, self.player1)

    def test_single_deal(self):
        dealer = self.player3
        turn = 1
        self.player4._cards.append(Card('Spades', 'A', 15))
        self.player1._cards.append(Card('Spades', '6', 6))
        self.player2._cards.append(Card('Diamonds', 'K', 14))
        self.player3._cards.append(Card('Clubs', '2', 2))
        trump = 'Spades'
        row = self.game.create_row(dealer)
        self.game.make_predictions(dealer, turn, trump)
        self.game.single_deal(row, trump)
        self.assertEqual(self.game._last_hand, self.player4)

    def test_calculate_points_successful_prediction(self):
        self.game._predictions[self.player3] = 3
        self.player3._hands = 3
        trump = 'Diamonds'
        self.game._score[self.player3] = 0
        self.game.calculate_points(self.player3, trump)
        self.assertEqual(self.game._score[self.player3], 19)

    def test_calculate_points_unsuccessful_prediction(self):
        self.game._predictions[self.player3] = 3
        self.player3._hands = 4
        trump = 'Diamonds'
        self.game._score[self.player3] = 0
        self.game.calculate_points(self.player3, trump)
        self.assertEqual(self.game._score[self.player3], 0)

    def test_calculate_points_no_trumps(self):
        self.game._predictions[self.player3] = 0
        self.player3._hands = 0
        trump = None
        self.game._score[self.player3] = 0
        self.game.calculate_points(self.player3, trump)
        self.assertEqual(self.game._score[self.player3], 50)

    def test_calculate_points_no_trumps_unsuccessful(self):
        self.game._predictions[self.player3] = 3
        self.player3._hands = 7
        trump = None
        self.game._score[self.player3] = 0
        self.game.calculate_points(self.player3, trump)
        self.assertEqual(self.game._score[self.player3], 0)


class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.player = AIPlayer('Player1')
        self.player2 = AIPlayer('Player2')
        self.player3 = AIPlayer('Player3')
        self.player4 = AIPlayer('Player4')
        self.jack_spades = Card('Spades', 'J', 12)
        self.five_spades = Card('Spades', '5', 5)
        self.ten_clubs = Card('Clubs', '10', 10)
        self.ace_spades = Card('Spades', 'A', 15)
        self.ace_diamonds = Card('Diamonds', 'A', 15)
        self.ace_clubs = Card('Clubs', 'A', 15)
        self.queen_hearts = Card('Hearts', 'Q', 13)
        self.five_hearts = Card('Hearts', '5', 5)
        self.six_hearts = Card('Hearts', '6', 6)
        self.player._cards.extend([self.jack_spades, self.five_spades,
                                   self.ten_clubs, self.ace_spades])

    def test_card_by_suite(self):
        by_suite = self.player.cards_by_suite('Spades')
        self.assertEqual(by_suite, [self.ace_spades, self.jack_spades,
                                    self.five_spades])

    def test_higher_cards_than(self):
        suite = 'Spades'
        value = 7
        higher_cards = self.player.higher_cards_than(suite, value)
        self.assertEqual(higher_cards, [self.ace_spades, self.jack_spades])

    def test_lower_cards_than(self):
        suite = 'Spades'
        value = 13
        lower_cards = self.player.lower_cards_than(suite, value)
        self.assertEqual(lower_cards, [self.jack_spades, self.five_spades])

    def test_points_from_aces(self):
        self.player._cards.extend([self.ace_clubs, self.ace_diamonds])
        points = self.player.points_from_aces()
        self.assertEqual(points, 3)

    def test_is_covered(self):
        self.player._cards.extend([self.queen_hearts, self.five_hearts,
                                   self.six_hearts])
        self.assertTrue(self.player.is_covered(self.queen_hearts))

    def test_is_covered_negative(self):
        self.assertFalse(self.player.is_covered(self.jack_spades))

    def test_points_from_covered_cards(self):
        self.player._cards.extend([self.ace_diamonds, self.ace_clubs,
                                   self.queen_hearts, self.five_hearts,
                                   self.six_hearts])
        self.assertEqual(self.player.points_from_covered_cards(), 1)

    def test_points_from_low_trumps(self):
        turn = 4
        trump = 'Spades'
        self.assertIn(self.player.points_from_low_trumps(turn, trump), [0, 1])

    def test_has_conflict(self):
        turn = 5
        predictions = {}
        predictions[self.player2] = 2
        predictions[self.player3] = 0
        predictions[self.player4] = 3
        self.assertTrue(self.player.has_conflict(turn, predictions))

    def test_resolved_conflict(self):
        hands = 1
        self.assertIn(self.player.resolved_conflict(hands), [0, 2])

    def test_choose_the_best_high(self):
        self.assertEqual(self.player.choose_the_best(True), self.ace_spades)

    def test_choose_the_best_low(self):
        self.assertEqual(self.player.choose_the_best(False), self.five_spades)

    def test_choose_from_others(self):
        self.assertEqual(self.player.choose_from_others(self.ace_diamonds,
                                                        'Spades'),
                         self.ten_clubs)

    def test_choose_highest_under(self):
        queen_spades = Card('Spades', 'Q', 13)
        self.assertEqual(self.player.choose_highest_under(queen_spades,
                                                          'Spades'),
                         self.jack_spades)

    def test_no_more_hands(self):
        cards_on_table = OrderedDict({})
        queen_spades = Card('Spades', 'Q', 13)
        trump = 'Clubs'
        cards_on_table[queen_spades] = self.player2
        cards_on_table[self.ace_diamonds] = self.player3
        cards_on_table[self.six_hearts] = self.player4
        self.assertEqual(self.player.no_more_hands(cards_on_table, trump),
                         self.jack_spades)

    def test_try_to_get_with_others(self):
        self.assertEqual(self.player.try_to_get_with_others(self.ace_diamonds,
                                                            'Hearts'),
                         self.five_spades)

    def test_try_to_get(self):
        queen_spades = Card('Spades', 'Q', 13)
        self.assertEqual(self.player.try_to_get(queen_spades,
                                                'Spades'),
                         self.ace_spades)

    def test_need_more_hands_first(self):
        cards_on_table = OrderedDict({})
        trump = 'Clubs'
        self.assertEqual(self.player.need_more_hands(cards_on_table, trump),
                         self.ace_spades)

    def test_need_more_hands_not_first(self):
        cards_on_table = OrderedDict({})
        queen_spades = Card('Spades', 'Q', 13)
        trump = 'Clubs'
        cards_on_table[queen_spades] = self.player2
        cards_on_table[self.ace_diamonds] = self.player3
        cards_on_table[self.six_hearts] = self.player4
        self.assertEqual(self.player.need_more_hands(cards_on_table, trump),
                         self.ace_spades)

    def test_give_card(self):
        cards_on_table = OrderedDict({})
        queen_spades = Card('Spades', 'Q', 13)
        trump = 'Clubs'
        cards_on_table[queen_spades] = self.player2
        cards_on_table[self.ace_diamonds] = self.player3
        cards_on_table[self.six_hearts] = self.player4
        self.player._prediction = 4
        self.player._hands = 3
        self.assertEqual(self.player.give_card(cards_on_table, trump),
                         self.ace_spades)


if __name__ == '__main__':
    unittest.main()
