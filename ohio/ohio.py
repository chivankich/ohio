from real_player import RealPlayer
from AIPlayer import AIPlayer
from game import Game


ivan = RealPlayer('Ivan')
marto = AIPlayer('Marto')
sando = AIPlayer('Sando')
kiss = AIPlayer('Kiss')

players = [ivan, marto, sando, kiss]

game = Game(players)
game.start()
