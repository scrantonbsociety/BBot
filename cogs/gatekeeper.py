import discord
from discord.ext import commands
from discord import app_commands
from db.currency import dbc
from db.user import dba
import decimal
class Gatekeeper(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    
    @app_commands.command()
    async def joined_when(self, interaction: discord.Interaction, user: discord.Member):
        joined_at = round(user.joined_at.timestamp())
        return await interaction.response.send_message(f'{user.name} joined the server <t:{joined_at}:D> <t:{joined_at}:T>')
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Gatekeeper(bot, bot.__getattribute__('dbapi')))
