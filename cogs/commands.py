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
    async def info(self, ctx):
        id = ctx.author.id
        rslt = await self.dblib.userExists(id)
        if rslt:
            await ctx.send("User Does Exist")
        else:
            await ctx.send("User Does Not Exist")
    # @commands.command()
    # async def register(self, ctx):
    #     id = ctx.author.id
    #     if database.userExists(id):
    #         await ctx.send("You have already been registered")
    #         return
    #     if database.register(id):
    #         await ctx.send("You have registered successfully")
    #     else:
    #         await ctx.send("Register Error")
async def setup(bot):
    await bot.add_cog(Commands(bot,bot.db,bot.dblib))
