from cgi import test
import discord
from mapping import Map
from discord.ext import commands

from discord import Embed

from cards import Card
from game import GameManager, Game

def load(bot: commands.Bot):
    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("Pong.")

    @bot.command()
<<<<<<< HEAD
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
=======
    async def maptest(ctx: commands.Context):
        testmap = Map("https://media.discordapp.net/attachments/949603786429698048/949640245215920178/Board.png?width=735&height=610")
        print(testmap)
        await ctx.send(str(testmap))
>>>>>>> 2c0ec75ccf216abd2e0565f15d140ec06acdba79
