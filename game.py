from hashlib import new
from cluecord.characters import Character
from player import Player
from deck import Deck
from rooms import Room
from weapons import Weapon
from re import L
from player import Player
from deck import Deck
from discord import TextChannel

class Game(object):
    """A game instance."""
    def __init__(self):
        self.players : list[Player] = []
        self.deck = Deck.generateDeck()

    def addPlayer(self, player : Player):
        self.players.append(player)

    def start(self):
        """Starts the game, shuffles cards to all players."""
        i = 0
        #for each card in deck
        while len(self.deck) > 0:
            #deal one to a player
            self.players[i].cards.append(Deck.pop(self.deck))
            #move onto next player
            i = i + 1
            #cycle back to original once end is reached
            if i >= len(self.players):
                i = 0

class GameManager(object):
    """Holds all Game instances."""
    games : "dict[TextChannel, Game]" = {}

    @staticmethod
    def hasGame(channel : TextChannel) -> bool:
        """Returns true if the GameManager has an instance for the provided channel."""
        return channel in GameManager.games.keys()

    def createGame(channel : TextChannel) -> Game:
        """Creates a new Game instance for the provided TextChannel."""
        newGame : Game = Game()
        GameManager.games[channel] = newGame
        return newGame

    def getGame(channel : TextChannel) -> Game:
        """Returns the Game instance for the provided TextChannel. Returns None if no instance exists."""
        return GameManager.games.get(channel)

    def endGame(channel : TextChannel):
        """Removes a Game instance from the GameManager."""
        GameManager.games.pop(channel)
