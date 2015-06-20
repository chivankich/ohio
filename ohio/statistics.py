class Statistics:
    def __init__(self, players):
        self.played = {'Spades': [], 'Hearts': [], 'Diamonds': [],
                       'Clubs': []}
        self.hands = {player: player._hands for player in players}



