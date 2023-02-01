from discord.ext import commands
class Commands(commands.Cog):
    def __init__(self, nbot):
        self.bot = nbot
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!!")

async def setup(bot):
    # print("hello world")
    await bot.add_cog(Commands(bot))
