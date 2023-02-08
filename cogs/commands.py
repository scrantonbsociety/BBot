from discord.ext import commands
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
        iid, reg = self.dblib.register(id)
        if reg:
            await ctx.send("Registered with iid {}".format(iid))
        else:
            await ctx.send("User already registered with iid {}".format(iid))
async def setup(bot):
    await bot.add_cog(Commands(bot,bot.db,bot.dblib))
