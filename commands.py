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
    async def start(ctx : commands.Context):
        if GameManager.hasGame(ctx.channel):
            await ctx.send("Game already in play in this channel.")
        else:
            GameManager.createGame(ctx.channel)
            await ctx.send("Started game.")

    @game.command()
    async def end(ctx : commands.Context):
        if GameManager.hasGame(ctx.channel):
            GameManager.endGame(ctx.channel)
            await ctx.send("Game ended.")
        else:
            await ctx.send("There is no game in play in this channel.")

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
        p2.setRoom(testmap.rooms[2])
        p3.setRoom(testmap.rooms[4])
        testmap.createMapImage([p1, p2, p3], "123")
        file = discord.File("123.png")
        embed = Embed()
        embed.title = "Board"
        embed.set_image(url="attachment://123.png")
        await ctx.send(file = file, embed = embed)

    @game.command()
    async def show(ctx : commands.Context):
        await ctx.send(GameManager.getGame(ctx.channel))
