from discord.ext import commands
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

async def setup(bot):
    await bot.add_cog(Commands(bot))
