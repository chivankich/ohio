class Card:
    def __init__(self, suite, rank, value):
        self._suite = suite
        self._rank = rank
        self._value = value

    def __repr__(self):
        return self._rank + ' ' + self._suite

    def __str__(self):
        return self._rank + ' ' + self._suite

    def __eq__(self, other):
        return [self._suite, self._value] == [other._suite, other._value]

    def __lt__(self, other):
        return self._value < other._value
