import discord
from discord.ext import commands
import json
token = ""
prefix = ""
with open("token.config","r") as f:
    token = json.load(f)["token"]
with open("bot.config","r") as f:
    prefix = json.load(f)["prefix"]
print(token)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("hey"):
        await message.channel.send("hi")
client.run(token)
bot = commands.Bot(prefix=prefix)