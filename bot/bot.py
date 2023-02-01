import discord
import asyncio
from discord.ext import commands
import json
token = ""
prefix = ""
bot = ""
def loadConfig():
    global token
    global prefix
    with open("token.config","r") as f:
        token = json.load(f)["token"]
    with open("bot.config","r") as f:
        prefix = json.load(f)["prefix"]
    # print(token)
    # print(prefix)
async def load():
    await bot.load_extension("commands")
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