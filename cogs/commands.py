from discord.ext import commands
from discord import User
from discord import app_commands
# from db.userlib import dba
import discord
class Commands(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    @app_commands.command()
    async def ping(self, interaction: discord.Integration):
        await interaction.response.send_message("Pong!!")
    @app_commands.command()
    async def stop(self, interaction: discord.Integration):
        await interaction.response.send_message("Stopping bot")
        await self.bot.close()
    @app_commands.command()
    async def id(self, interaction: discord.Integration, user: User = None):
        if user==None:
            user = interaction.user
        id = user.id
        rslt = self.dbapi.user.get(id)
        if rslt!=None:
            await interaction.response.send_message("The ID of user ``{}``  is ``{}``".format(user.name,rslt))
        else:
            await interaction.response.send_message("User Does Not Exist")
    @app_commands.command()
    async def register(self, interaction: discord.Integration, user: User = None):
        if user==None:
            user = interaction.user
        pid = self.dbapi.user.get(user.id)
        if(pid==None):
            iid = self.dbapi.user.register(user.id)
            await interaction.response.send_message("Created a new ID ``{}`` for user ``{}``".format(iid,user.name))
        else:
            await interaction.response.send_message("User ``{}`` already registered with id ``{}``".format(user.name,pid))
    @app_commands.command()
    async def deregister(self, interaction: discord.Integration, user: User = None):
        if user==None:
            user = interaction.user
        if self.dbapi.user.unregister(user.id):
            await interaction.response.send_message("User ``{}`` unregistered".format(user.name))
        else:
            await interaction.response.send_message("User ``{}`` is not registered".format(user.name))
    @commands.command()
    async def forcesync(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            await self.bot.tree.sync()
            await ctx.send("Sync updated commands to the client")
        else:
            await ctx.send("You are not authorized to run this cmd")
    @app_commands.command()
    async def sync(self, interaction: discord.Integration):
        if interaction.user.id in self.bot.config["owners"]:
            await self.bot.tree.sync()
            await interaction.response.send_message("Sync updated commands to the client")
        else:
            await interaction.response.send_message("You are not authorized to run this cmd")

    @app_commands.command()
    async def slash(self, interaction: discord.Integration):
        await interaction.response.send_message("slash command test")
async def setup(bot):
    await bot.add_cog(Commands(bot,bot.dbapi))
