from discord.ext import commands
from discord import User
from discord import app_commands
# from db.userlib import dba
import discord
class Commands(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
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
        rslt = self.dbapi.user.get(id)
        if rslt!=None:
            await ctx.send("The ID of user ``{}``  is ``{}``".format(user.name,rslt))
        else:
            await ctx.send("User Does Not Exist")
    @commands.command()
    async def register(self, ctx, user: User = None):
        if user==None:
            user = ctx.author
        pid = self.dbapi.user.get(user.id)
        if(pid==None):
            iid = self.dbapi.user.register(user.id)
            await ctx.send("Created a new ID ``{}`` for user ``{}``".format(iid,user.name))
        else:
            await ctx.send("User ``{}`` already registered with id ``{}``".format(user.name,pid))
    @commands.command()
    async def deregister(self, ctx, user: User = None):
        if user==None:
            user = ctx.author
        if self.dbapi.user.unregister(user.id):
            await ctx.send("User ``{}`` unregistered".format(user.name))
        else:
            await ctx.send("User ``{}`` is not registered".format(user.name))
    @commands.command()
    async def sync(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            await self.bot.tree.sync()
            await ctx.send("Sync updated commands to the client")
        else:
            await ctx.send("You are not authorized to run this cmd")
    @app_commands.command()
    async def slash(self, interaction: discord.Integration):
        await interaction.response.send_message("slash command test")
async def setup(bot):
    await bot.add_cog(Commands(bot,bot.dbapi))
