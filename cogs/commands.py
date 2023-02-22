from discord.ext import commands
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
    async def id(self, ctx):
        id = ctx.author.id
        rslt = self.dblib.getUser(id)
        if rslt!=None:
            await ctx.send("User IID is {}".format(rslt))
        else:
            await ctx.send("User Does Not Exist")
    @commands.command()
    async def register(self, ctx):
        id = ctx.author.id
        iid = self.dblib.register(id)
        await ctx.send("iid for user is {}".format(iid))
    @commands.command()
    async def deregister(self, ctx):
        id = ctx.author.id
        if self.dblib.unregister(id):
            await ctx.send("User successfully unregistered")
        else:
            await ctx.send("User not registered")
async def setup(bot):
    await bot.add_cog(Commands(bot,bot.db,dba(bot.db)))
