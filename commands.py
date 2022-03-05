def load(bot: commands.Bot):
    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("Pong.")