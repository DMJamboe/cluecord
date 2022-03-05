from cgi import test
import discord
from mapping import Map
from discord.ext import commands

from discord import Embed

from cards import Card
from game import GameManager, Game
from characters import Character
from player import Player

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
        elif len(players) < 1 or len(players) > 6:
            await ctx.send("Invalid number of players")
        else:
            game = GameManager.createGame(ctx.channel)
            for player in players:
                game.addPlayer(player)
            currentGame = GameManager.getGame(ctx.channel)
            currentGame.start()
            await ctx.send("Game started")
            currentGame.map.createMapImage(currentGame.players, ctx.channel.id)
            file = discord.File(str(ctx.channel.id) + ".jpg")
            embed = Embed()
            embed.title = "Board"
            embed.set_image(url="attachment://" + str(ctx.channel.id) + ".jpg")
            await ctx.send(file=file, embed=embed)
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
