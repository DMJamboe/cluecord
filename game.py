from tkinter import Button
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
        self.accusations = []

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

    def currentPlayer(self) -> Player:
        return self.players[0]


    async def turn(self) -> bool:
        """Takes a turn, returns True if the game has been won."""
        player = self.currentPlayer()

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
    game = GameManager.getGame(interaction.channel)
    user = interaction.user
    currentPlayer = game.currentPlayer()
    if user != currentPlayer.user:
        await interaction.response.send_message(content="It is not your turn.", ephemeral=True)
    action = ""
    if buttonID == "movebutton":
        await moveAction(interaction)
        action = "move"
    if buttonID == "guessbutton":
        guessAction(interaction)
        action = "guess"
    if buttonID == "accusebutton":
        await accuseAction(interaction)
        action = "accuse"
    await interaction.message.edit(view=None, content=game.currentPlayer().character.name + " has chosen to " + action)

async def moveAction(interaction : discord.Interaction):
    currentGame = GameManager.getGame(interaction.channel)
    currentPlayer = currentGame.currentPlayer()
    currentRoom = currentPlayer.getRoom()
    print(currentPlayer)
    print(currentRoom)
    embed = Embed()
    moveView = discord.ui.View()
    rooms = []
    for roomKey in currentRoom.connections:
        moveView.add_item(discord.ui.Button(label=roomKey, style=discord.ButtonStyle.secondary, custom_id=roomKey))
        rooms.append(currentRoom.connections[roomKey])
    moveView.interaction_check = movementPressed
    await interaction.response.send_message(view=moveView, ephemeral=True)

async def movementPressed(interaction : discord.Interaction):
    #await interaction.response.defer()
    await interaction.response.edit_message(view=None, content="Moving...")
    print(interaction.data)
    buttonID = interaction.data.get("custom_id")
    game = GameManager.getGame(interaction)
    user = interaction.user
    currentGame = GameManager.getGame(interaction.channel)
    currentPlayer = currentGame.currentPlayer()
    currentRoom = currentPlayer.getRoom()
    currentPlayer.setRoom(currentRoom.connections[buttonID])
    # Update board
    currentGame.map.createMapImage(currentGame.players, interaction.channel.id)
    file = discord.File(str(interaction.channel.id) + ".jpg")
    embed = Embed()
    embed.title = "Board"
    embed.set_image(url="attachment://" + str(interaction.channel.id) + ".jpg")
    await interaction.channel.send(file = file, embed = embed, content=currentPlayer.character.name + " has moved into the " + str(currentRoom.connections[buttonID]))
    

def guessAction(interaction : discord.Interaction):
    pass

async def accuseAction(interaction : discord.Interaction):
    #take in accusation
    characterMenu = discord.ui.Select(custom_id="characterMenu", placeholder=None, min_values=1, max_values=1, options=generateCharacterOptions(), disabled=False, row=None)

    #send options to user
    menuView = discord.ui.View(characterMenu)
    menuView.interaction_check = accusationsMade
    game = GameManager.getGame(interaction.channel)
    
    await interaction.response.send_message(view=menuView, ephemeral=True)

    #check if accurate
    #send message to user (and possibly end game)
    
async def accusationsMade(interaction : discord.Interaction) :
    """Take an accusation and check if valid"""
    if interaction.data.get("custom_id") == "characterMenu":
        weaponMenu = discord.ui.Select(custom_id="weaponMenu", placeholder=None, min_values=1, max_values=1, options=generateWeaponOptions(), disabled=False, row=None)
        menuView = discord.ui.View(weaponMenu)
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get('values')[0])
        menuView.interaction_check = accusationsMade
        await interaction.response.send_message(view=menuView, ephemeral=True)
    if interaction.data.get("custom_id") == "weaponMenu":
        roomMenu = discord.ui.Select(custom_id="roomMenu", placeholder=None, min_values=1, max_values=1, options=generateRoomOptions(), disabled=False, row=None)
        menuView = discord.ui.View(roomMenu)
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get('values')[0])
        menuView.interaction_check = accusationsMade
        await interaction.response.send_message(view=menuView, ephemeral=True)
    if interaction.data.get("custom_id") == "roomMenu":
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get('values')[0])
        print(game.accusations)
        if game.envelope == game.accusations :
            await interaction.response.send_message(content="You win!",ephemeral=True)
        else :
            await interaction.response.send_message(content="You don't win!",ephemeral=True)
        game.accusations = []




        


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