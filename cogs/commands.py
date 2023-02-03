from discord.ext import commands
import discord
from misc import database
class Commands(commands.Cog):
    def __init__(self, nbot):
        self.bot = nbot
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!!")
    @commands.command()
    async def stop(self, ctx):
        await ctx.send("Stopping bot")
        await ctx.bot.close()
    @commands.command()
    async def info(self, ctx):
        id = ctx.author.id
        await ctx.send(database.userExists(id))
    @commands.command()
    async def register(self, ctx):
        id = ctx.author.id
        if database.userExists(id):
            await ctx.send("You have already been registered")
            return
        if database.register(id):
            await ctx.send("You have registered successfully")
        else:
            await ctx.send("Register Error")
async def setup(bot):
    await bot.add_cog(Commands(bot))
