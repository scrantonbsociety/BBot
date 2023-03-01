from discord.ext import commands
from discord import User
from db.currency import dbc
from db.dblib import dba
import decimal
class Currency(commands.Cog):
    def __init__(self, nbot, dbc, dba):
        self.bot = nbot
        self.dbc = dbc
        self.dba = dba
    @commands.command()
    async def bal(self, ctx, user: User = None):
        if user!=None:
            iid = self.dba.getUser(user.id)
        else:
            iid = self.dba.getUser(ctx.author.id)
        if iid!=None:
            rslt = self.dbc.checkBal(iid,"bot.currency")
        else:
            rslt = 0
        await ctx.send(rslt)
    @commands.command()
    async def pay(self, ctx, user: User, amnt: float):
        iid = self.dba.getUser(ctx.author.id)
        diid = self.dba.getUser(user.id)
        if diid==None:
            diid = self.dba.register(user.id)
        if iid==None:
            await ctx.send("User Not Registered")
        amount = round(amnt,2)
        if self.dbc.deductCurrency(iid,"bot.currency",amount):
            self.dbc.addCurrency(diid,"bot.currency",amount)
            await ctx.send("currency transfer successful")
        else:
            await ctx.send("currency transfer failed")
        

async def setup(bot):
    await bot.add_cog(Currency(bot,dbc(bot.db),dba(bot.db)))
