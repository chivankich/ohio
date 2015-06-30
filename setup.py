from game import Game
from real_player import RealPlayer
from ai_player import AIPlayer
from ui import CLI


class CLIOhio:
    @staticmethod
    def start():
        CLI.clear_window()

        print()
        print('Hi, you might want to play Ohio?!')
        print()
        print('OK, how many people will play? (from 1 to 4)')
        number = input('==> ')
        while not CLI.is_number(number) or int(number) not in range(0, 5):
            CLI.clear_window()
            print()
            print('Hi, you might want to play Ohio?!')
            print()
            print('Please, enter a number from 1 to 4!')
            number = input('==> ')

        players = []
        number = int(number)
        for n in range(1, number + 1):
            CLI.clear_window()
            print()
            print('Please, enter a name for the ' + str(n) + ' player: ')
            name = input('==> ')
            players.append(RealPlayer(name))

        for n in range(1, 5 - number):
            players.append(AIPlayer('AIRobot' + str(n)))

        CLI.clear_window()
        print()
        print('Players are ready to play!')
        print()
        for player in players:
            print(player._name)

        game = Game(players)

        print()
        ok = input('Press any key to start the game...')

        game.start()
