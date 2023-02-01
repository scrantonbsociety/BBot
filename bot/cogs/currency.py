import discord
import json
import random
from discord.ext import commands
class Currency(commands.Cog):
    def __init__(self, nbot):
        self.bot = nbot
        self.ans = {}
    async def newMath(self, channel):
        num0 = random.randint(3,12)
        num1 = random.randint(3,12)
        self.ans[str(channel)] = num0+num1
        channel = self.bot.get_channel(channel)
        await channel.send("{} + {} = ?".format(num0,num1))
    @commands.Cog.listener()
    async def on_ready(self):
        with open("bot.config","r") as f:
            self.mathChannels = json.load(f)["workChannels"]
        for chan in self.mathChannels:
            await self.newMath(chan)
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.channel.id in self.mathChannels:
            try:
                num = int(message.content)
            except:
                return
            if self.ans[str(message.channel.id)] == num:
                await self.newMath(message.channel.id)

async def setup(bot):
    await bot.add_cog(Currency(bot))
