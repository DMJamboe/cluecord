from player import Player
from cards import Card
from characters import Character
from mapping import Map
from deck import generateDeck, generateCharacters, Deck
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
    action = ""
    if buttonID == "movebutton":
        await moveAction(interaction)
        action = "move"
    if buttonID == "guessbutton":
        guessAction(interaction)
        action = "guess"
    if buttonID == "accusebutton":
        accuseAction(interaction)
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
    print(interaction.data)
    buttonID = interaction.data.get("custom_id")
    currentGame = GameManager.getGame(interaction.channel)
    currentPlayer = currentGame.currentPlayer()
    currentRoom = currentPlayer.getRoom()
    currentPlayer.setRoom(currentRoom.connections[buttonID])
    # Update board
    currentGame.map.createMapImage(currentGame.players, interaction.channel)
    file = discord.File(str(interaction.channel) + ".png")
    embed = Embed()
    embed.title = "Board"
    embed.set_image(url="attachment://" + str(interaction.channel) + ".png")
    await interaction.channel.send(file = file, embed = embed, content=currentPlayer.character.name + " has moved into the " + currentRoom.connections[buttonID])
        
def guessAction(interaction : discord.Interaction):
    pass

def accuseAction(interaction : discord.Interaction):
    pass

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