import imp
from characters import Character
from weapons import Weapon
from rooms import Room
import random

class Deck(object):
    """The deck of cards"""
    def __init__(self, characterList : "list[Character]" , weaponList : "list[Weapon]", roomList : "list[Room]"):
        self.cards = []
        self.envelope = generateEnvelope(characterList , weaponList, roomList)
        

        #add characters
        for character in characterList:
            self.cards.append(character)
        #add weapons
        for weapon in weaponList:
            self.cards.append(weapon)
        #add rooms
        for room in roomList:
            self.cards.append(room)

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)

    def pop(self):
        """Return the first card from the deck (removing it from the deck)"""
        return self.cards.pop()

    
def generateDeck() -> Deck:
        """Create a shuffled deck of all cards"""
        characters = generateCharacters("data/characters.txt")
        rooms = generateRooms("data/rooms.txt")
        weapons = generateWeapons("data/weapons.txt")
        deck = Deck(characters, rooms, weapons)
        Deck.shuffle(deck)
        return deck
    
def generateCharacters(filename: str) -> "list[Character]":
        """Create a list of character objects"""
        characters = []
        with open(filename, "r") as f:
            for character in f:
                data = character.split()
                characters.append(Character(data[0], data[1], data[2]))
        return characters

def generateRooms(filename: str) -> "list[Room]":
    """Create a list of room objects"""
    rooms = []
    with open(filename, "r") as f:
        for room in f:
            data = room.split()
            rooms.append(Room(data[0], data[1]))
    return rooms

def generateWeapons(filename: str) -> "list[Weapon]":
    """Create a list of weapon objects"""
    weapons = []
    with open(filename, "r") as f:
        for weapon in f:
            data = weapon.split(",")
            weapons.append(Weapon(data[0], data[1]))
    return weapons

def generateEnvelope(characterList : "list[Character]" , weaponList : "list[Weapon]", roomList : "list[Room]"):
    """Generate an envelope of form [Character, Weapon, Room]"""
    envelope = []
    #create envelope
    random.shuffle(characterList)
    random.shuffle(weaponList)
    random.shuffle(roomList)
    self.envelope.append(characterList.pop())
    self.envelope.append(weaponList.pop())
    self.envelope.append(roomList.pop())

    return envelope
