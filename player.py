import discord
from cards import Card
from characters import Character
from rooms import Room

class Player(object):
    """A user playing the game."""
    def __init__(self, user : discord.User, character : Character):
        self.user : discord.User = user
        self.cards : list[Card] = []
        self.character : Character = character
        self.location : Room = None

    def __str__(self):
        return f"User: {self.user}\nCards: {self.cards}\nCharacter: {self.character}\nLocation: {self.location}"

    def setRoom(self, room : Room):
        self.location = room