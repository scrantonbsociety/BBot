import discord
from discord.ext import commands
from discord import User
from discord import app_commands
import random
class Currency(commands.Cog):
    def __init__(self, nbot, dbapi):
        self.bot = nbot
        self.dbapi = dbapi
    @app_commands.command()
    async def bal(self, integration: discord.Integration, user: User = None):
        if user!=None:
            iid = self.dbapi.user.get(user.id)
        else:
            iid = self.dbapi.user.get(integration.user.id)
        if iid!=None:
            rslt = self.dbapi.currency.bal(iid,"bot.currency")
        else:
            rslt = 0
        await integration.response.send_message(rslt)
    @app_commands.command()
    async def pay(self, integration: discord.Integration, user: User, amnt: float):
        iid = self.dbapi.user.get(integration.user.id)
        diid = self.dbapi.user.get(user.id)
        if diid==None:
            diid = self.dbapi.user.register(user.id)
        if iid==None:
            await integration.response.send_message("User Not Registered")
        amount = round(amnt,2)
        if self.dbapi.currency.deduct(iid,"bot.currency",amount):
            self.dbapi.currency.add(diid,"bot.currency",amount)
            await integration.response.send_message("currency transfer successful")
        else:
            await integration.response.send_message("currency transfer failed")
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
            await integration.response.send_message("Not enough money to bet!")
            return None
        if 'h' in call.lower():
            call = '0'
        else:
            call = '1'
        if side == int(call):
            await integration.response.send_message("Congratulations! You won {}".format(amount*2))
            self.dbapi.currency.add(iid,"bot.currency",amount*2)
        else:
            await integration.response.send_message("Sorry! You lost your money.")
    @app_commands.command()
    async def bj(self, integration: discord.Integration, wager: float):
        user = integration.user
        iid = self.dbapi.user.get(user.id)
        if not self.dbapi.currency.deduct(iid,"bot.currency", wager):
            await integration.response.send_message("Not enough money to bet!")
            return None
        # This function follows the established naming convention, and there's no changing it
        cards = ['aceOfSpades', 'twoOfSpades', 'threeOfSpades', 'fourOfSpades', 'fiveOfSpades', 'sixOfSpades', 'sevenOfSpades', 'eightOfSpades', 'nineOfSpades', 'tenOfSpades', 'jackOfSpades', 'queenOfSpades', 'kingOfSpades'
                 'aceOfDiamonds', 'twoOfDiamonds', 'threeOfDiamonds', 'fourOfDiamonds', 'fiveOfDiamonds', 'sixOfDiamonds', 'sevenOfDiamonds', 'eightOfDiamonds', 'nineOfDiamonds', 'tenOfDiamonds', 'jackOfDiamonds', 'queenOfDiamonds', 'kingOfDiamonds'
                 'aceOfClubs', 'twoOfClubs', 'threeOfClubs', 'fourOfClubs', 'fiveOfClubs', 'sixOfClubs', 'sevenOfClubs', 'eightOfClubs', 'nineOfClubs', 'tenOfClubs', 'jackOfClubs', 'queenOfClubs', 'kingOfClubs'
                 'aceOfHearts', 'twoOfHearts', 'threeOfHearts', 'fourOfHearts', 'fiveOfHearts', 'sixOfHearts', 'sevenOfHearts', 'eightOfHearts', 'nineOfHearts', 'tenOfHearts', 'jackOfHearts', 'queenOfHearts', 'kingOfHearts']
        dealerDeck = [cards.pop(random.randint(0, len(cards))), cards.pop(random.randint(0, len(cards)))]
        playerDeck = [cards.pop(random.randint(0, len(cards))), cards.pop(random.randint(0, len(cards)))]

        # This method does not work for the case: A 5 5 A
        # As it would return 22 instead of 12
        def evaluateAces(deck, total):
            aceValue = 11 
            for card in deck:
                if 'ace' in card:
                    # If the total goes over 21, hard set the value of aces to 1 and reevaluate.
                    if total + 11 > 21:
                        aceValue = 1
                    total += aceValue
            return total

        def getDeckSum(deck):
            sum = 0
            for card in deck:
                if 'two' in card:
                    sum += 2
                elif 'three' in card:
                    sum += 3
                elif 'four' in card:
                    sum += 4
                elif 'five' in card:
                    sum += 5
                elif 'six' in card:
                    sum += 6
                elif 'seven' in card:
                    sum += 7
                elif 'eight' in card:
                    sum += 8
                elif 'nine' in card:
                    sum += 9
                elif 'ten' in card or 'jack' in card or 'queen' in card or 'king' in card:
                    sum += 10
            sum = evaluateAces(deck, sum)
            return sum

        # Three scenarios:
        # Dealer has natural - Game ends immediately and bet is collected
        # Player has natural - Game ends immediately and bet and a half is paid back
        # Both dealer and player has natural - Game ends immediately and bet is paid back

        dealerTotal = getDeckSum(dealerDeck)
        playerTotal = getDeckSum(playerDeck)

        # Need to make sure the dealer only checks for blackjack if a 10-value card is the up card
        # If the up card is an ace, offer insurance
        if dealerTotal == 21 and playerTotal == 21:
            await integration.response.send_message("We both have blackjack! Game over.")
            self.dbapi.currency.add(iid,"bot.currency", wager)
            return None
        elif dealerTotal == 21 and playerTotal != 21:
            await integration.response.send_message("Dealer has blackjack! Thanks for playing!")
            return None
        elif dealerTotal != 21 and playerTotal == 21:
            await integration.response.send_message("Congratulations! You have blackjack!")
            self.dbapi.currency.add(iid,"bot.currency", wager * 1.5)
            return None
        
        def displayDeck(deck):
            response = "Your cards:\n"
            for card in deck:
                response += card + "\n"
            return response
        
        await integration.response.send_message("Your cards:\n{}\n{}\nDealer has {}, do you hit or stay?".format(playerDeck[0], playerDeck[1], dealerDeck[0]))
        
        # Retrieve input from the player to hit or stay

        inPlay = True
        while inPlay:
            await integration.response.send_message(displayDeck(playerDeck) + "\nDo you hit or stay?")
            if True: # Player choses to hit
                # Order is imporant because it is true to the game
                playerDeck.append(cards.pop(random.randint(0, len(cards))))
                playerTotal = getDeckSum(playerDeck)
                if playerTotal == 21:
                    await integration.response.send_message("You drew a {}! Blackjack! Congratulations!".format(playerDeck[len(playerDeck-1)]))

                    return None
                elif playerTotal > 21:
                    await integration.response.send_message("You drew a {}! You've gone bust! Thank you for playing.".format(playerDeck[len(playerDeck-1)]))
                    return None
        # When the player stands, repeat this process for the dealer and program corresonding outcomes


async def setup(bot):
    await bot.add_cog(Currency(bot,bot.dbapi))
