Ohio
====

A realization of a simple game with cards, which is not popular, but very interesting, though.

##Rules
Rules are simple:

- On every round you should guess exactly how many hands will you take, no more, no less.
- There are 16 rounds, 12 with arbitrary chosen trump (a suit that beat all other suits) and 4 rounds without trump.
- The more powerful card is the Ace, after that the King, Queen, Jack, 10 and so on down to 2.
- On first level players are dealt one card, on second level two cards and so on. On the last round all cards are dealt.
- The player after the dealer starts. Every next player must respond with card of the same suit if possible. Otherwise, every card is a possible response.
- Trumps are more powerful that other suits. The best card given wins the hand.
- If you managed to make as many hands as you have guessed, the formula for your result is `10 + x * x`, where `x` is the number of hands you made.
- But on the last four rounds, if you take zero hands and have declared to do so, you get 50 points (because it's very difficult not to get a hand with 13 cards).

The game is designed to be played by 4 players, but you can play alone or with just one or two friends, if you substitute the remaining seats with robots.

##Requirements
All you need is a Python 3.4.X and Git, running on your system.

####Python
- You can download and install the relevant sources or binaries from [python.org/downloads](https://www.python.org/downloads).

####Git
- Download Git for the appropriate platform from the [git-scm.com/downloads](https://git-scm.com/downloads)

##Setup
The first thing you need to do is to clone the git project in any folder to your system. Open the command line (in Windows) or the terminal (in Linux) and execute the following command:

`git clone https://github.com/chivankich/ohio.git`

This will clone the repo with all the necessary stuff.

Enter in the _ohio_ directory. To start the game, just execute `python play.py` in the console. That will start the CLI mode of the game.

(TODO: GUI is expected in the future)

##Tests
You can run the unittests by executing the following command in the project directory:

`python tests.py`

##License
The license, provided in the project is GNU GPL.