import discord
from discord.ext import commands
class Work(commands.Cog):
    def __init__(self, nbot):
        self.bot = nbot
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content.startswith("hi"):
            await message.channel.send("ho")

async def setup(bot):
    await bot.add_cog(Work(bot))
