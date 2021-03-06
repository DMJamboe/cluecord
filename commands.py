from cgi import test
import discord
from mapping import Map
from discord.ext import commands

from discord import Embed

from cards import Card
from game import GameManager, Game
from characters import Character
from player import Player
from weapons import Weapon
from rooms import Room

def load(bot: commands.Bot):
    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("Pong.")

    @bot.command()
    async def pringle(ctx : commands.Context):
        print("Pringle.")

    @bot.command()
    async def testcard(ctx : commands.Context):
        test = Card("Dagger", f"https://image.invaluable.com/housePhotos/Sofe/87/589087/H20136-L96012319.jpg")
        embed = Embed()
        embed.title = test.getName()
        embed.set_image(url=test.getImagePath())
        await ctx.send(embed=embed)

    @bot.group(
        help = "Possible Commands",
        brief="These are the commands for the game"
    )
    async def game(ctx : commands.Context):
        pass

    @game.command(
        help = "start",
        brief = "Use as !game start @player ... to start the game"

    )
    async def start(ctx : commands.Context, *players : discord.User):
        if GameManager.hasGame(ctx.channel):
            await ctx.send("Game already in play in this channel.")
        elif len(players) < 2 or len(players) > 6:
            await ctx.send("Invalid number of players")
        else:
            game = GameManager.createGame(ctx.channel)
            for player in players:
                if player in [player.user for player in game.players]:
                    await ctx.send("Cannot have more than one of the same player in one game!")
                    GameManager.endGame(ctx.channel)
                    return
                if GameManager.gameOf(player) != None:
                    await ctx.send("Cannot have users in multiple games at once!")
                    GameManager.endGame(ctx.channel)
                    return
                game.addPlayer(player)
            currentGame = GameManager.getGame(ctx.channel)

            currentGame.start()
            startEmbed = discord.embeds.Embed()
            startMessage = ""
            for player in currentGame.players:
                startMessage=startMessage+player.user.name+" as "+player.character.name+"\n"
            startMessage = startMessage
            startEmbed.add_field(name = "The game begins!", value=startMessage)
            await ctx.send(embed=startEmbed) #"Game started.\nPlease check your dm's to see your hand.")

            # DMs players their hand
            
            for player in currentGame.players:
                embed = discord.embeds.Embed()
                embed.title = player.character.getName()
                embed.description = "I can disprove the following pieces of evidence"
                if player.user.dm_channel == None:
                    await player.user.create_dm()
                characters_text = ""
                for card in player.cards:
                    if isinstance(card, Character):
                        characters_text += "??? " + card.name + "\n"
                embed.add_field(name="People", value=characters_text, inline=True)
                weapons_text = ""
                for card in player.cards:
                    if isinstance(card, Weapon):
                        weapons_text += "??? " + card.name + "\n"
                embed.add_field(name="Weapons", value=weapons_text, inline=True)
                rooms_txt = ""
                for card in player.cards:
                    if isinstance(card, Room):
                        rooms_txt += "??? " + card.name + "\n"            
                embed.add_field(name="Rooms", value=rooms_txt, inline=True)
                embed.color = discord.Color.from_rgb(hex_to_rgb(player.character.colour)[0], hex_to_rgb(player.character.colour)[1], hex_to_rgb(player.character.colour)[2])
                await player.user.dm_channel.send(embed=embed)

            await GameManager.getGame(ctx.channel).turn()

    @game.command(
        help = "end",
        brief = "Use as !game end to end a game"
    )
    async def end(ctx : commands.Context):
        if GameManager.hasGame(ctx.channel):
            GameManager.endGame(ctx.channel)
            await ctx.send("Game ended.")
        else:
            await ctx.send("There is no game in play in this channel.")

    @game.command(
        help = "turn",
        brief = "Use as !game turn to take your turn"
    )
    async def turn(ctx : commands.Context):
        await GameManager.getGame(ctx.channel).turn()

    @game.command(
        help = "rules",
        brief = "Use as !game rules to check the rules"
    )
    async def rules(ctx : commands.Context):
        embed = discord.embeds.Embed()
        embed.title = "Rules"
        embedMessage = "Players take it in turns to choose one of the follwing options:\nAccuse - Pick a place, weapon and person and accuse them of being the criminal. Warning: a bad accusation will result in your loss.\nMove - You may choose a new location to move to.\nGuess - Pick a person and weapon and ask if anyone can prove they didn't commit the murder in your current room."
        embed.add_field(name = "How to play:", value=embedMessage)
        await ctx.send(embed=embed)

    @bot.command()
    async def maptest(ctx: commands.Context):
        testmap = Map("https://media.discordapp.net/attachments/949603786429698048/949640245215920178/Board.png?width=735&height=610")
        print(testmap)
        await ctx.send(str(testmap))

    @bot.command()
    async def drawtest(ctx: commands.Context):
        testmap = Map("https://media.discordapp.net/attachments/949603786429698048/949640245215920178/Board.png?width=735&height=610")
        testmap.testImage()
        file = discord.File("123.png")
        embed = Embed()
        embed.title = "Board"
        embed.set_image(url="attachment://123.png")
        await ctx.send(file = file, embed = embed)

    @bot.command()
    async def drawtest2(ctx: commands.Context):
        testmap = Map("https://media.discordapp.net/attachments/949603786429698048/949640245215920178/Board.png?width=735&height=610")
        scarlett = Character("Mrs. Scarlett", "image/path", "#FF0000")
        plumb = Character("Mr. Plumb", "image/path", "#6a0dad")
        peacock = Character("Mrs. Peacock", "image/path", "#0000FF")
        p1 = Player("1", scarlett)
        p2 = Player("2", plumb)
        p3 = Player("3", peacock)
        p1.setRoom(testmap.rooms[2])
        p2.setRoom(testmap.rooms[7])
        p3.setRoom(testmap.rooms[7])
        testmap.createMapImage([p1, p2, p3], "123")
        file = discord.File("123.png")
        embed = Embed()
        embed.title = "Board"
        embed.set_image(url="attachment://123.png")
        await ctx.send(file = file, embed = embed)
    
    @bot.command()
    async def testUserInput(ctx : commands.Context, *users : discord.User):
        await ctx.send(content=users[1].name)


def hex_to_rgb(hex : str) -> "tuple[int]":
    """Code credited to https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python"""
    stripped = hex.lstrip("#")
    return tuple(int(stripped[i:i+2], 16) for i in (0, 2, 4))