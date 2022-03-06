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

    @bot.group()
    async def game(ctx : commands.Context):
        pass

    @game.command()
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
                game.addPlayer(player)
            currentGame = GameManager.getGame(ctx.channel)

            currentGame.start()
            startEmbed = discord.embeds.Embed()
            startMessage = ""
            for player in currentGame.players:
                startMessage=startMessage+player.user.name+" as "+player.character.name+"\n"
            startEmbed.add_field(name = "The game begins!", value=startMessage)
            await ctx.send(embed=startEmbed) #"Game started.\nPlease check your dm's to see your hand.")

            # DMs players their hand
            
            for player in currentGame.players:
                embed = discord.embeds.Embed()
                if player.user.dm_channel == None:
                    await player.user.create_dm()
                text = "Characters:\n"
                for card in player.cards:
                    if isinstance(card, Character):
                        text += card.name + "\n"
                text += "\nWeapons:\n"
                for card in player.cards:
                    if isinstance(card, Weapon):
                        text += card.name + "\n"
                text += "\nRooms:\n"
                for card in player.cards:
                    if isinstance(card, Room):
                        text += card.name + "\n"            
                embed.add_field(name="Your Hand", value=text)    
                await player.user.dm_channel.send(embed=embed)

            await GameManager.getGame(ctx.channel).turn()

    @game.command()
    async def end(ctx : commands.Context):
        if GameManager.hasGame(ctx.channel):
            GameManager.endGame(ctx.channel)
            await ctx.send("Game ended.")
        else:
            await ctx.send("There is no game in play in this channel.")

    @game.command()
    async def show(ctx : commands.Context):
        await ctx.send(GameManager.getGame(ctx.channel))

    @game.command()
    async def turn(ctx : commands.Context):
        await GameManager.getGame(ctx.channel).turn()

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
