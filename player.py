import discord
from cards import Card

class Player(object):
    """A user playing the game."""
    def __init__(self, user : discord.User):
        self.user : discord.User = user
        self.cards : list[Card] = []