from game import Game
from real_player import RealPlayer
from AIPlayer import AIPlayer
from ui import CLI


class CLIOhio:
    @staticmethod
    def start():
        CLI.clear_window()

        print('Hi, you might want to play Ohio?!')
        number = input('OK, how many people will play? (from 1 to 4) ')
        while not CLI.is_number(number) or int(number) not in range(0, 5):
            CLI.clear_window()
            print('Hi, you might want to play Ohio?!')
            number = input('Please, enter a number from 1 to 4! ')

        players = []
        number = int(number)
        for n in range(1, number + 1):
            CLI.clear_window()
            name = input('Please, enter a name for the ' + \
                         str(n) + ' player: ')
            players.append(RealPlayer(name))

        for n in range(1, 5 - number):
            players.append(AIPlayer('AIRobot' + str(n)))

        CLI.clear_window()
        print('Players are ready to play!')
        for player in players:
            print(player._name)

        game = Game(players)

        ok = input('Type OK to start the game!')
        while ok.lower() != 'ok':
            CLI.clear_window()
            print('Players are ready to play!')
            for player in players:
                print(player._name)
            ok = input('Please, type OK to start the game!')

        game.start()
