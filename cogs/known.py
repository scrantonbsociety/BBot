from discord.ext import commands
from discord import User
from discord import app_commands
import discord
class Known(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    @app_commands.command()
    async def knownas(self, interaction: discord.Integration, title: str, type: str, iid: str):
        if interaction.user.id in self.bot.config["owners"]:
            rslt = self.dbapi.known.add(title,type,iid)
            if rslt != iid:
                await interaction.response.send_message("Something went wrong with the known as")
            else:
                await interaction.response.send_message("``{}`` labeled as ``{}`` successfully".format(title,iid))
        else:
            await interaction.response.send_message("User not authorized")
    @app_commands.command()
    async def name(self, interaction: discord.Integration, title: str, type: str):
        name = self.dbapi.known.lookup(title,type)
        if name=="":
            await interaction.response.send_message("name ``{}`` is not known".format(title))
        else:
            await interaction.response.send_message("name ``{}`` is known as ``{}``".format(title, name))
    @app_commands.command()
    async def names(self, interaction: discord.Interaction, iid: str, type: str):
        names = self.dbapi.known.lookupnames(iid,type)
        if len(names)==0:
            await interaction.response.send_message("internal id ``{}`` not found in db".format(iid))
        else:
            listOfNames = ""
            for name in names:
                listOfNames+=name + "\n"
            listOfNames = listOfNames[:-1]
            await interaction.response.send_message("The following names were found for the internal id ``{}`` ```\n{}```".format(iid, listOfNames))    

async def setup(bot):
    await bot.add_cog(Known(bot,bot.dbapi))
