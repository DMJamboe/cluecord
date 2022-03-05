from cgi import test
import discord
from mapping import Map
from discord.ext import commands

def load(bot: commands.Bot):
    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("Pong.")

    @bot.command()
    async def maptest(ctx: commands.Context):
        testmap = Map("https://media.discordapp.net/attachments/949603786429698048/949640245215920178/Board.png?width=735&height=610")
        print(testmap)
        await ctx.send(str(testmap))