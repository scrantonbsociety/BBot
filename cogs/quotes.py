from discord.ext import commands
from discord import app_commands
import discord
class Quotes(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi


    #probably want to add in the name found in known to the quotes database so
    #it is easier to search, remove, and list quotes, but I'm not sure why
    #I am unable to use found instead of name when adding the quote to the database
    @app_commands.command()
    async def quote_add(self, interaction: discord.Interaction, name: str, quote: str):
        if len(quote)>1024 or len(name)>128:
            await interaction.response.send_message("Quote or name of quoted is too long!")
            return
        found = self.dbapi.known.lookup(name, "person") #probably should refactor to have a method search for the name
        if(found != ""):
            rslt = self.dbapi.quotes.add(found,quote,str(interaction.user.id))
            await interaction.response.send_message("Quote: " + quote + " - " + name)
            return rslt
        else:
            await interaction.response.send_message("Quoted person not found!")
            return
        
    #@app_commands.command()
        # async def removeQuote(self, interaction: discord.Interaction, quoted: str) #should the user specify the quoted person, or the id of the person who submitted the quote
        #     if(self.dbapi.quotes.get(quoted)):
        #        rslt = self.dbapi.quotes.remove(quoted):
        #        await interaction.response.send_message("Removed quote: " + rslt)
        #     else:
        #         await interaction.response.send_message("Quote not found")


    # @app_commands.command()
    # async def list_quotes(self, interaction: discord.Interaction, person: str):
        # quotes = self.dbapi.quotes.list(person)
        # if():
            # await interaction.response.send_message("internal id ``{}`` not found in db")
        # else:
            # quoteList = ""
        # for quote in quotes:
                # quoteList+=quote + "\n"
            # quoteList = quoteList[:-1]
            # await interaction.response.send_message("The following names were found for the internal id ``{}`` ```\n{}```".format(quoteList))


async def setup(bot):
    await bot.add_cog(Quotes(bot,bot.dbapi))

    #call wellknown from cogs; as person look up iid
    #deleting quotes should only be bot owner, admin, and person who wrote the quote