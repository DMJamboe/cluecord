from player import Player
from cards import Card
from characters import Character
from mapping import Map
from deck import generateDeck, generateCharacters, Deck, generateRooms, generateWeapons
from discord import TextChannel, User, Embed
import discord

class Game(object):
    """A game instance."""
    def __init__(self, channel : TextChannel):
        self.channel = channel
        self.players : list[Player] = []
        self.deck = generateDeck()
        self.envelope : tuple[Card] = self.deck.envelope
        self.characterList : list[Character] = generateCharacters("data/characters.txt")
        self.map = Map("https://media.discordapp.net/attachments/949603786429698048/949685135538806854/Board.png?width=757&height=607")

    def __str__(self):
        return f"Players: {self.players}\nEnvelope: {self.envelope}"
        
    def addPlayer(self, user : User):
        self.players.append(Player(user, self.characterList.pop(0))) # TODO - check character list populated

    def start(self):
        """Starts the game, shuffles cards to all players."""
        self.deck.shuffle()
        self.deck.deal(self.players)
        [player.setRoom(self.map.getStartingRoom()) for player in self.players]

    def nextPlayer(self) -> Player:
        r = self.players.pop(0)
        self.players.append(r)
        return r

    async def turn(self) -> bool:
        """Takes a turn, returns True if the game has been won."""
        player = self.nextPlayer()

        # player is presented with options 'Accusation', 'Guess' or 'Move'
        embed = Embed()
        accuseButton = discord.ui.Button(label="Accuse", style=discord.ButtonStyle.danger, custom_id="accusebutton")
        guessButton = discord.ui.Button(label="Guess", style=discord.ButtonStyle.primary, custom_id="guessbutton")
        moveButton = discord.ui.Button(label="Move", style=discord.ButtonStyle.secondary, custom_id="movebutton")
        turnView = discord.ui.View(moveButton, guessButton, accuseButton)

        turnView.interaction_check = turnButtonPressed

        await self.channel.send(view=turnView)

        # if accusation, player is presented with options of Character, Weapon and Room

        # if guess, player is presented with options of Character and Weapon

        # if move, player is presented with options of rooms to move to

async def turnButtonPressed(interaction : discord.Interaction):
    buttonID = interaction.data.get("custom_id")
    game = GameManager.getGame(interaction)
    user = interaction.user
    if buttonID == "movebutton":
        moveAction(interaction)
    if buttonID == "guessbutton":
        guessAction(interaction)
    if buttonID == "accusebutton":
        await accuseAction(interaction)

def moveAction(interaction : discord.Interaction):
    pass

def guessAction(interaction : discord.Interaction):
    pass

async def accuseAction(interaction : discord.Interaction):
    #take in accusation
    characterMenu = discord.ui.Select(custom_id="characterMenu", placeholder=None, min_values=1, max_values=1, options=generateCharacterOptions(), disabled=False, row=None)
    #send options to user
    menuView = discord.ui.View(characterMenu, weaponMenu, roomMenu)

    menuView.interaction_check = None

    await interaction.channel.send(view=menuView)

    #check if accurate
    #send message to user (and possibly end game)
    

def generateCharacterOptions() -> "list[discord.SelectOption()]" :
    """Generate select option list of all characters"""
    options = []
    allcharacters = generateCharacters("data/characters.txt")

    for character in allcharacters :
        options.append(discord.SelectOption(label=character.name, description=None, default=False))
    
    return options

def generateWeaponOptions() -> "list[discord.SelectOption()]" :
    """Generate select option list of all weapons"""
    options = []
    allWeapons = generateWeapons("data/weapons.txt")

    for weapon in allWeapons :
        options.append(discord.SelectOption(label=weapon.name, description=None, default=False))
    
    return options

def generateRoomOptions() -> "list[discord.SelectOption()]" :
    """Generate select option list of all rooms"""
    options = []
    allRooms = generateRooms("data/rooms.txt")

    for room in allRooms :
        options.append(discord.SelectOption(label=room.name, description=None, default=False))
    
    return options



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