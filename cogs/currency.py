from discord.ext import commands
from db.currency import dbc
from db.dblib import dba
class Currency(commands.Cog):
    def __init__(self, nbot, dbc, dba):
        self.bot = nbot
        self.dbc = dbc
        self.dba = dba
    @commands.command()
    async def bal(self, ctx):
        iid = self.dba.getUser(ctx.author.id)
        rslt = self.dbc.checkBal(iid,"bot.currency")
        await ctx.send(rslt)
async def setup(bot):
    await bot.add_cog(Currency(bot,dbc(bot.db),dba(bot.db)))
