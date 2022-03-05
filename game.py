from player import Player
from deck import Deck

class Game(object):
    """A game instance."""
    def __init__(self, channel : TextChannel):
        self.channel = channel
        self.players : list[Player] = []
        self.deck = Deck()

    def addPlayer(self, player : Player):
        self.players.append(player)

    def start(self):
        """Starts the game, shuffles cards to all players."""
