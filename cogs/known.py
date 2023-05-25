from discord.ext import commands
from discord import app_commands
import discord
class Known(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    known_group = app_commands.Group(name="known", description="A set of mostly admin commands which allow the user to associate internal ids with external names")
    @known_group.command(name="as")
    async def kas(self, integration: discord.Integration, title: str, iid: str):
        if integration.user.id in self.bot.config["owners"]:
            rslt = self.dbapi.known.add(title,iid,integration.user.id)
            if rslt != iid:
                await integration.response.send_message("Something went wrong with the known as")
            else:
                await integration.response.send_message("``{}`` labeled as ``{}`` successfully".format(title,iid))
        else:
            await integration.response.send_message("User not authorized")
    @known_group.command()
    async def name(self, integration: discord.Integration, title: str, type: str):
        name = self.dbapi.known.lookup(title,type)
        if name=="":
            await integration.response.send_message("name ``{}`` is not known".format(title))
        else:
            await integration.response.send_message("name ``{}`` is known as ``{}``".format(title, name))
    @known_group.command()
    async def names(self, integration: discord.Integration, iid: str):
        names = self.dbapi.known.lookupnames(iid)
        if len(names)==0:
            await integration.response.send_message("internal id ``{}`` not found in db".format(iid))
        else:
            listOfNames = ""
            for name in names:
                listOfNames+=name + "\n"
            listOfNames = listOfNames[:-1]
            await integration.response.send_message("The following names were found for the internal id ``{}`` ```\n{}```".format(iid, listOfNames))    
    @app_commands.command()
    async def othername(self, integration: discord.Integration, currentname: str, newname: str):
        nameId = self.dbapi.known.lookup(currentname,"")
        if nameId=="":
            await integration.response.send_message("name ``{}`` does not exist".format(currentname))
        else:
            if self.dbapi.known.lookup(newname,"")=="":
                await integration.response.send_message("name ``{}`` is already in use".format(newname))
            else:
                self.dbapi.known.add(newname.lower(),nameId,integration.user.id)
                await integration.response.send_message("name ``{}`` associated with name ``{}``".format(newname,currentname))
async def setup(bot):
    await bot.add_cog(Known(bot,bot.dbapi))
