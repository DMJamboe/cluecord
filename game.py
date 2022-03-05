from hashlib import new
from cluecord.characters import Character
from player import Player
from deck import Deck
from rooms import Room
from weapons import Weapon

class Game(object):
    """A game instance."""
    def __init__(self, channel : TextChannel):
        self.channel = channel
        self.players : list[Player] = []
        self.deck = generateDeck()

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

def generateDeck():
        """Create a shuffled deck of all cards"""
        characters = generateCharacters("characters.txt")
        rooms = generateRooms("rooms.txt")
        weapons = generateWeapons("weapons.txt")
        deck = Deck(characters, rooms, weapons)
        Deck.shuffle(deck)
        return deck
    
def generateCharacters(filename: str):
        """Create a list of character objects"""
        characters = []
        with open(filename, "r") as f:
            for character in f:
                data = character.split()
                characters.append(Character(data[0], data[1], data[2]))
        return characters

def generateRooms(filename: str):
    """Create a list of room objects"""
    rooms = []
    with open(filename, "r") as f:
        for room in f:
            data = room.split()
            rooms.append(Room(data[0], data[1]))
    return rooms

def generateWeapons(filename: str):
    """Create a list of weapon objects"""
    weapons = []
    with open(filename, "r") as f:
        for weapon in f:
            data = weapon.split()
            weapons.append(Weapon(data[0], data[1]))
    return weapons

    


