import discord
from discord.ext import commands
from discord import User
from discord import app_commands
from db.currency import dbc
from db.user import dba
import decimal
import random
class Currency(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    @commands.command()
    async def bal(self, ctx, user: User = None):
        if user!=None:
            iid = self.dbapi.user.get(user.id)
        else:
            iid = self.dbapi.user.get(ctx.author.id)
        if iid!=None:
            rslt = self.dbapi.currency.bal(iid,"bot.currency")
        else:
            rslt = 0
        await ctx.send(rslt)
    @commands.command()
    async def pay(self, ctx, user: User, amnt: float):
        iid = self.dbapi.user.get(ctx.author.id)
        diid = self.dbapi.user.get(user.id)
        if diid==None:
            diid = self.dbapi.user.register(user.id)
        if iid==None:
            await ctx.send("User Not Registered")
        amount = round(amnt,2)
        if self.dbapi.currency.deduct(iid,"bot.currency",amount):
            self.dbapi.currency.add(diid,"bot.currency",amount)
            await ctx.send("currency transfer successful")
        else:
            await ctx.send("currency transfer failed")
    @app_commands.command()
    async def bf(self, integration: discord.Integration, amnt: float, call: str):
        # Future suggestions:
        # Make Discord suggest to the user the only available options they can input
        # Yell at the user for putting in anything else
        user = integration.user # Refers to Discord's user object
        iid = self.dbapi.user.get(user.id) #Gets internal id of the user from our db
        amount = round(amnt, 2) #Rounds the amount correctly
        if self.dbapi.currency.deduct(iid,"bot.currency", amount):
            side = random.randint(0, 1) #flips the coin, 0 = heads - 1 = tails
        else:
            await integration.response.send_message("No money to bet!")
        if 'h' in call.lower():
            call = '0'
        else:
            call = '1'
        if side == int(call):
            await integration.response.send_message("Congratulations! You won {}".format(amount*2))
            self.dbapi.currency.add(iid,"bot.currency",amount*2)
        else:
            await integration.response.send_message("Sorry! You lost your money.")

async def setup(bot):
    await bot.add_cog(Currency(bot,bot.dbapi))
