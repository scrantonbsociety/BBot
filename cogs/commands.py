from discord.ext import commands
from discord import User
from db.dblib import dba
import discord
class Commands(commands.Cog):
    def __init__(self, nbot, db, dblib):
        self.bot = nbot
        self.db = db
        self.dblib = dblib
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!!")
    @commands.command()
    async def stop(self, ctx):
        await ctx.send("Stopping bot")
        await ctx.bot.close()
    @commands.command()
    async def id(self, ctx, user: User = None):
        if user==None:
            user = ctx.author
        id = user.id
        rslt = self.dblib.getUser(id)
        if rslt!=None:
            await ctx.send("The ID of user ``{}``  is ``{}``".format(user.name,rslt))
        else:
            await ctx.send("User Does Not Exist")
    @commands.command()
    async def register(self, ctx, user: User = None):
        if user==None:
            user = ctx.author
        pid = self.dblib.getUser(user.id)
        if(pid==None):
            iid = self.dblib.register(user.id)
            await ctx.send("Created a new ID ``{}`` for user ``{}``".format(iid,user.name))
        else:
            await ctx.send("User ``{}`` already registered with id ``{}``".format(user.name,pid))
    @commands.command()
    async def deregister(self, ctx, user: User = None):
        if user==None:
            user = ctx.author
        if self.dblib.unregister(user.id):
            await ctx.send("User ``{}`` unregistered".format(user.name))
        else:
            await ctx.send("User ``{}`` is not registered".format(user.name))
async def setup(bot):
    await bot.add_cog(Commands(bot,bot.db,dba(bot.db)))
