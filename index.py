import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv

import commands as botcommands

# load environment variables
load_dotenv()
TOKEN = os.environ.get("TOKEN")

# set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discordbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# set up bot
bot = commands.Bot(command_prefix="!")

# add bot commands
botcommands.load(bot) # loads commands defined in the commands module
print("Bot running.")
# init bot
bot.run(TOKEN)

