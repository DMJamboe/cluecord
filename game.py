from msvcrt import getch
from re import L
from player import Player
from deck import Deck
from cards import Card
from characters import getCharacters, Character
from mapping import Map
import deck
from discord import TextChannel, User

class Game(object):
    """A game instance."""
    def __init__(self, channel : TextChannel):
        self.channel = channel
        self.players : list[Player] = []
        self.deck = deck.generateDeck()
        self.envelope : tuple[Card] = self.deck.envelope
        self.characterList : list[Character] = getCharacters()
        self.map = Map()

    def __str__(self):
        return f"Players: {self.players}\nEnvelope: {self.envelope}"
        
    def addPlayer(self, user : User):
        self.players.append(Player(user, self.characterList.pop(0))) # TODO - check character list populated

    def start(self):
        """Starts the game, shuffles cards to all players."""
        self.deck.shuffle()
        self.deck.deal(self.players)
        [player.setRoom(self.map.getStartingRoom()) for player in self.players]

    



class GameManager(object):
    """Holds all Game instances."""
    games : "dict[TextChannel, Game]" = {}

    @staticmethod
    def hasGame(channel : TextChannel) -> bool:
        """Returns true if the GameManager has an instance for the provided channel."""
        return channel in GameManager.games.keys()

    def createGame(channel : TextChannel) -> Game:
        """Creates a new Game instance for the provided TextChannel."""
        newGame : Game = Game(channel)
        GameManager.games[channel] = newGame
        return newGame

    def getGame(channel : TextChannel) -> Game:
        """Returns the Game instance for the provided TextChannel. Returns None if no instance exists."""
        return GameManager.games.get(channel)

    def endGame(channel : TextChannel):
        """Removes a Game instance from the GameManager."""
        GameManager.games.pop(channel)