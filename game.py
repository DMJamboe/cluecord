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
        self.accusectr = 0
        self.guessctr = 0

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
    
    def kickCurrentPlayer(self):
        self.players.pop(0)

    def currentPlayer(self) -> Player:
        return self.players[0]

    async def attemptDisprove(self):
        playerMatch = None
        cardsMatch = []
        for player in self.players[1:]:
            for card in self.accusations:
                if card in [card.getName() for card in player.cards]:
                    playerMatch = player
                    cardsMatch.append(card)
        if len(cardsMatch) == 0:
            await guessAction(None, player=self.currentPlayer())
        else:
            options = [discord.SelectOption(label=card, description=None, default=False) for card in cardsMatch]
            optionsMenu = discord.ui.Select(custom_id="optionsMenu", placeholder=None, min_values=1, max_values=1, options=options, disabled=False, row=None)
            cardsView = discord.ui.View(optionsMenu)
            if (playerMatch.user.dm_channel is None):
                playerMatch.user.create_dm()
            cardsView.interaction_check = guessAction
            await playerMatch.user.dm_channel.send(f"Choose a card to show {self.currentPlayer().user.name}", view=cardsView)

    async def turn(self) -> bool:
        """Takes a turn, returns True if the game has been won."""
        player = self.currentPlayer()

        await self.channel.send(content = "It is " + player.user.mention + "'s turn, they are " + player.character.name)

        # Checks if the player has won by default
        if len(self.players) == 1:
            await self.channel.send(content = player.user.name + " wins!")
            GameManager.endGame(self.channel)
            return

        self.map.createMapImage(self.players, self.channel.id)
        file = discord.File(str(self.channel.id) + ".jpg")
        embed = Embed()
        embed.title = "Board"
        embed.set_image(url="attachment://" + str(self.channel.id) + ".jpg")

        await self.channel.send(file=file, embed=embed)

        # player is presented with options 'Accusation', 'Guess' or 'Move'
        embed = Embed()
        accuseButton = discord.ui.Button(label="Accuse", style=discord.ButtonStyle.danger, custom_id="accusebutton")
        guessButton = discord.ui.Button(label="Guess", style=discord.ButtonStyle.primary, custom_id="guessbutton")
        moveButton = discord.ui.Button(label="Move", style=discord.ButtonStyle.secondary, custom_id="movebutton")
        turnView = discord.ui.View(moveButton, guessButton, accuseButton)

        turnView.interaction_check = turnButtonPressed

        await self.channel.send(view=turnView)

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
        await guessAction(interaction)
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
    user = interaction.user
    currentGame = GameManager.getGame(interaction.channel)
    currentPlayer = currentGame.currentPlayer()
    currentRoom = currentPlayer.getRoom()
    currentPlayer.setRoom(currentRoom.connections[buttonID])
    currentGame.nextPlayer()
    await currentGame.turn()

async def guessAction(interaction : discord.Interaction, player=None):
    if interaction is not None and interaction.data.get("custom_id") != "optionsMenu":
        game = GameManager.getGame(interaction.channel)
    if interaction == None:
        game = GameManager.gameOf(player.user)
        await game.channel.send(f"Nobody can refute this guess.")
        game.accusations = []
        game.nextPlayer()
        await game.turn()
    elif interaction.data.get("custom_id") == "optionsMenu":
        await interaction.response.edit_message(view=None)
        game = GameManager.gameOf(interaction.user)
        player = list(filter(lambda player: player.user == interaction.user, game.players))[0]
        if game.currentPlayer().user.dm_channel is None:
            game.currentPlayer().user.create_dm()
        await game.channel.send(f"{player.character.name} whispers to {game.currentPlayer().character.name}")
        msg_embed = Embed()
        msg_embed.title = f"{player.character.name} whispers to you..."
        msg_embed.description = "I know it wasn't " + interaction.data.get("values")[0]
        msg_embed.color = discord.Color.from_rgb(hex_to_rgb(player.character.colour)[0], hex_to_rgb(player.character.colour)[1], hex_to_rgb(player.character.colour)[2])
        await game.currentPlayer().user.dm_channel.send(embed=msg_embed)
        game.accusations = []
        game.nextPlayer()
        await game.turn()

    elif interaction.data.get("custom_id") == "characterMenu":
        if game.guessctr != 0:
            return
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get("values")[0])
        weaponMenu = discord.ui.Select(custom_id="weaponMenu", placeholder=None, min_values=1, max_values=1, options=generateWeaponOptions(), disabled=False, row=None)
        listView = discord.ui.View(weaponMenu)
        listView.interaction_check = guessAction
        game.guessctr += 1
        await interaction.response.send_message(content=f"> in the {game.currentPlayer().location.getName()} with the...", view=listView, ephemeral=True)
    elif interaction.data.get("custom_id") == "weaponMenu":
        if game.guessctr != 1:
            return
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get("values")[0])
        game.accusations.append(game.currentPlayer().location.getName())
        game.guessctr = 0
        await interaction.channel.send(f"I think it was {game.accusations[0]} with the {game.accusations[1]} in the {game.accusations[2]}")
        await game.attemptDisprove()
        await interaction.response.defer()
    else:
        game.guessctr = 0
        characterMenu = discord.ui.Select(custom_id="characterMenu", placeholder=None, min_values=1, max_values=1, options=generateCharacterOptions(), disabled=False, row=None)
        listView = discord.ui.View(characterMenu)
        listView.interaction_check = guessAction
        await interaction.response.send_message(content="> I think it was...", view=listView, ephemeral=True)

async def accuseAction(interaction : discord.Interaction):
    game = GameManager.getGame(interaction.channel)
    game.accusectr = 0
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
    game = GameManager.getGame(interaction.channel)
    if interaction.data.get("custom_id") == "characterMenu":
        if game.accusectr != 0:
            return
        weaponMenu = discord.ui.Select(custom_id="weaponMenu", placeholder=None, min_values=1, max_values=1, options=generateWeaponOptions(), disabled=False, row=None)
        menuView = discord.ui.View(weaponMenu)
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get('values')[0])
        menuView.interaction_check = accusationsMade
        game.accusectr += 1
        await interaction.response.send_message(view=menuView, ephemeral=True)
    if interaction.data.get("custom_id") == "weaponMenu":
        if game.accusectr != 1:
            return
        roomMenu = discord.ui.Select(custom_id="roomMenu", placeholder=None, min_values=1, max_values=1, options=generateRoomOptions(), disabled=False, row=None)
        menuView = discord.ui.View(roomMenu)
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get('values')[0])
        menuView.interaction_check = accusationsMade
        game.accusectr += 1
        await interaction.response.send_message(view=menuView, ephemeral=True)
    if interaction.data.get("custom_id") == "roomMenu":
        if game.accusectr != 2:
            return
        game = GameManager.getGame(interaction.channel)
        game.accusations.append(interaction.data.get('values')[0])
        print(game.accusations)
        game.accusectr = 0
        print(game.envelope)
        if game.envelope[0].getName() == game.accusations[0] and game.envelope[2].getName() == game.accusations[1] and game.envelope[1].getName() == game.accusations[2] :
            await interaction.channel.send(content=game.currentPlayer().character.name + " wins!")
            GameManager.endGame(interaction.channel)
        else :
            await interaction.channel.send(content=game.currentPlayer().character.name + " guessed incorrectly! They have been kicked from the game :(")

            game.kickCurrentPlayer()
            await game.turn()
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

    def gameOf(user : discord.User):
        """Returns a Game instance if a given user is in it."""
        activeGames = list(filter(lambda game : user in [player.user for player in game.players], GameManager.games.values()))
        if len(activeGames) > 0:
            return activeGames[0]
        else:
            return None

def hex_to_rgb(hex : str) -> "tuple[int]":
    """Code credited to https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python"""
    stripped = hex.lstrip("#")
    return tuple(int(stripped[i:i+2], 16) for i in (0, 2, 4))