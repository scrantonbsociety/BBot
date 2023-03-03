import discord
import asyncio
from discord.ext import commands
import json
import os
from db import dbapi
from db import database
token = ""
dblogin = {}
prefix = ""
bot = ""
def loadConfig():
    global token
    global prefix
    global dblogin
    with open("auth.config","r") as f:
        config = json.load(f)
    token = config["token"]
    dblogin = config["sql"]
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
    db = database.db(dblogin)
    db.connect()
    bot.assignDB(db)
    bot.assignDBAPI(dbapi.dbint(db))
    cogs = findAllCogs("cogs")
    print("{} cogs".format(len(cogs)))
    for cog in cogs:
        await bot.load_extension(cog)
    print("cogs loaded")
class DBBOT(commands.Bot):
    def assignDB(self, db):
        self.db = db
    def assignDBAPI(self,dbapi):
        self.dbapi = dbapi
loadConfig()
intents = discord.Intents.default()
intents.message_content = True
bot = DBBOT(command_prefix=prefix, intents=intents)
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