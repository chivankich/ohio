import os


class CLI:
    @staticmethod
    def is_number(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def clear_window():
        if os.name.lower() == 'nt':
            command = 'cls'
        else:
            command = 'clear'

        return os.system(command)

    @staticmethod
    def overview(turn, trump, predictions, row, score, cards):
        CLI.clear_window()

        print('Round: ', str(turn))
        print()

        points = sorted(list(score.items()), key=lambda item: item[1],
                        reverse=True)
        print('Score:'.center(85))
        print('-' * 85)
        print('|', end='')
        for item in points:
            print(item[0]._name.center(20) + '|', end='')
        print()
        print('-' * 85)
        print('|', end='')
        for item in points:
            print(str(item[1]).center(20) + '|', end='')
        print()
        print('-' * 85)
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
                print((str(predictions[player]) + ' hands').center(20) + \
                      '|', end='')
            else:
                print('thinking...'.center(20) + '|', end='')
        print()
        print('-' * 85)
        print()

        print('Your cards:'.center(12), 'Trump:'.center(12), sep=' ' * 10)
        print('-' * 12 + ' ' * 10 + '-' * 12)
        print(str(cards[0]).center(12) + '|', '|' + trump.center(12) + \
              '|', sep=' ' * 8)
        print('-' * 12, '-' * 12, sep=' ' * 10)
        for card in cards[1:]:
            print(str(card).center(12) + '|')
            print('-' * 12)
        print()

    @staticmethod
    def situation(cards_on_table, trump, turn, row, score, cards):
        CLI.clear_window()

        print('Round: ', str(turn))
        print()

        points = sorted(list(score.items()), key=lambda item: item[1],
                        reverse=True)
        print('Score:'.center(85))
        print('-' * 85)
        print('|', end='')
        for item in points:
            print(item[0]._name.center(20) + '|', end='')
        print()
        print('-' * 85)
        print('|', end='')
        for item in points:
            print(str(item[1]).center(20) + '|', end='')
        print()
        print('-' * 85)
        print()

        print('Cards on the table:'.center(85))
        print('-' * 85)
        print('|', end='')
        for player in row:
            print((player._name + ' (' + str(player._hands) + '/' + \
                  str(player._prediction) +')').center(20) + '|', end='')
        print()
        print('-' * 85)
        print('|', end='')
        for card in list(cards_on_table.keys()):
            print(str(card).center(20) + '|', end='')
        print()
        print('-' * 85)
        print()

        print('Your cards:'.center(12), 'Trump:'.center(12), sep=' ' * 10)
        print('-' * 12 + ' ' * 10 + '-' * 12)
        print(str(cards[0]).center(12) + '|', '|' + trump.center(12) + \
              '|', sep=' ' * 8)
        print('-' * 12, '-' * 12, sep=' ' * 10)
        for card in cards[1:]:
            print(str(card).center(12) + '|')
            print('-' * 12)
        print()

