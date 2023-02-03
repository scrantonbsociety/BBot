import discord
import asyncio
from discord.ext import commands
import json
import os
token = ""
prefix = ""
bot = ""
def loadConfig():
    global token
    global prefix
    with open("auth.config","r") as f:
        token = json.load(f)["token"]
    with open("bot.config","r") as f:
        prefix = json.load(f)["prefix"]
def findAllCogs(fname):
    clist = []
    if os.path.isdir(fname):
        for path in os.listdir(fname):
            clist = clist + findAllCogs(fname + "\\" + path)
        return clist
    else:
        if fname.endswith(".py"):
            return [fname.replace("\\",".")[:-3]]
        else:
            return []
async def load():
    cogs = findAllCogs("cogs")
    print("{} cogs".format(len(cogs)))
    for cog in cogs:
        await bot.load_extension(cog)
    print("cogs loaded")
loadConfig()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
asyncio.run(load())
bot.run(token)
@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("hey"):
        await message.channel.send("hi")