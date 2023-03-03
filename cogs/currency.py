from discord.ext import commands
from discord import User
from db.currency import dbc
from db.user import dba
import decimal
class Currency(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    @commands.command()
    async def bal(self, ctx, user: User = None):
        if user!=None:
            iid = self.dbapi.user.getUser(user.id)
        else:
            iid = self.dbapi.user.getUser(ctx.author.id)
        if iid!=None:
            rslt = self.dbapi.currency.checkBal(iid,"bot.currency")
        else:
            rslt = 0
        await ctx.send(rslt)
    @commands.command()
    async def pay(self, ctx, user: User, amnt: float):
        iid = self.dbapi.user.getUser(ctx.author.id)
        diid = self.dbapi.user.getUser(user.id)
        if diid==None:
            diid = self.dbapi.user.register(user.id)
        if iid==None:
            await ctx.send("User Not Registered")
        amount = round(amnt,2)
        if self.dbapi.currency.deductCurrency(iid,"bot.currency",amount):
            self.dbapi.currency.addCurrency(diid,"bot.currency",amount)
            await ctx.send("currency transfer successful")
        else:
            await ctx.send("currency transfer failed")
        

async def setup(bot):
    await bot.add_cog(Currency(bot,bot.dbapi))
