import discord
from discord.ext import commands
from discord import User
from discord import app_commands
import random
import asyncio
""" from PIL import Image
import os """
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
    @app_commands.choices(call=[
        app_commands.Choice(name="Heads", value=True),
        app_commands.Choice(name="Tails", value=False)
    ])
    async def bf(self, integration: discord.Integration, amnt: float, call: app_commands.Choice[int]):
        # Future suggestions:
        # Make Discord suggest to the user the only available options they can input
        # Yell at the user for putting in anything else
        user = integration.user # Refers to Discord's user object
        iid = self.dbapi.user.get(user.id) #Gets internal id of the user from our db
        message = "You called " + str(call.value) + "!\n" # message to be sent after flip
        amount = round(amnt, 2) #Rounds the amount correctly
        if self.dbapi.currency.deduct(iid,"bot.currency", amount):
            side = random.randint(0, 1) #flips the coin, 0 = heads - 1 = tails
        else:
            await integration.response.send_message("Not enough money to bet!")
            return None
        result = True if side == 0 else False
        message += "The coin landed on " + str(result) + "!\n"
        if call.value == result:
            message += "Congratulations! You won {}".format(amount*2)
            self.dbapi.currency.add(iid,"bot.currency",amount*2)
        else:
            message += "Sorry! You lost your money."
        await integration.response.send_message(message)
    @app_commands.command()
    async def bj(self, integration: discord.Integration, wager: float):
        # This function follows the established naming convention, and there's no changing it
        user = integration.user
        iid = self.dbapi.user.get(user.id)
        if not self.dbapi.currency.deduct(iid,"bot.currency", wager):
            await integration.response.send_message("Not enough money to bet!")
            return None

        cards = ['aceOfSpades', 'twoOfSpades', 'threeOfSpades', 'fourOfSpades', 'fiveOfSpades', 'sixOfSpades', 'sevenOfSpades', 'eightOfSpades', 'nineOfSpades', 'tenOfSpades', 'jackOfSpades', 'queenOfSpades', 'kingOfSpades',
                 'aceOfDiamonds', 'twoOfDiamonds', 'threeOfDiamonds', 'fourOfDiamonds', 'fiveOfDiamonds', 'sixOfDiamonds', 'sevenOfDiamonds', 'eightOfDiamonds', 'nineOfDiamonds', 'tenOfDiamonds', 'jackOfDiamonds', 'queenOfDiamonds', 'kingOfDiamonds',
                 'aceOfClubs', 'twoOfClubs', 'threeOfClubs', 'fourOfClubs', 'fiveOfClubs', 'sixOfClubs', 'sevenOfClubs', 'eightOfClubs', 'nineOfClubs', 'tenOfClubs', 'jackOfClubs', 'queenOfClubs', 'kingOfClubs',
                 'aceOfHearts', 'twoOfHearts', 'threeOfHearts', 'fourOfHearts', 'fiveOfHearts', 'sixOfHearts', 'sevenOfHearts', 'eightOfHearts', 'nineOfHearts', 'tenOfHearts', 'jackOfHearts', 'queenOfHearts', 'kingOfHearts']
        
        # The standard in casinos if anywhere from 4-8 decks of cards
        masterDeck = cards + cards + cards + cards
        
        def drawCard():
            return masterDeck.pop(random.randint(0, len(cards)-1))
            
        faceCards = ['jack', 'queen', 'king']
        dealerDeck = [drawCard(), drawCard()]
        playerDeck = [drawCard(), drawCard()]
        #playerDeck = ['twoOfSpades', 'twoOfDiamonds'] # For debugging split choice
        #dealerDeck = ['aceOfSpades', drawCard()] # For debugging insurance choice
        #dealerDeck = ['aceOfSpades', 'tenOfHearts']
        #playerDeck = ['aceOfSpades', 'twoOfDiamonds']

        def getDeckSum(hand):
            sum = 0
            hasAce = False
            for card in hand:
                if 'ace' in card:
                    sum += 11
                    hasAce = True
                elif 'two' in card:
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
                elif 'ten' in card or card[0:card.index("Of")] in faceCards:
                    sum += 10
                if hasAce and sum > 21:
                    sum -= 10
            return sum
        
        def displayDeck(deck, isDealer):
            response = ""
            if isDealer:
                response += "Dealer's cards:\n"
            else:
                response += "Player cards:\n"
            for card in deck:
                response += card + "\n"
            return response
        
        dealerTotal = getDeckSum(dealerDeck)
        playerTotal = getDeckSum(playerDeck)

        if playerTotal == 21:
            gameEndMessage = displayDeck(playerDeck, False) + displayDeck(dealerDeck, True)
            # If dealer also has blackjack, hand is a push
            if dealerTotal == 21:
                gameEndMessage += "You and the dealer both have blackjack! Hand is a push!\nThanks for playing!"
                self.dbapi.currency.add(iid,"bot.currency", wager)
            # If dealer does not have blackjack, pay 1.5 wager and end game
            else:
                gameEndMessage += f"Congratulations, you have blackjack!\nYou won {1.5 * wager}!"
                self.dbapi.currency.add(iid,"bot.currency", (1.5 * wager))
            await integration.response.send_message(gameEndMessage)
            return None
        
        insurancePlaced = False
        deckSplit = False

        """ def renderHandImage(hand):


            playingcardImgPath = '/cogs/images/playingcards/'

            for card in hand:


            embed = discord.Embed(
                title = 'Blackjack Game',
                description = 'Testing',
                color = 0x481a6b
            ).set_image(playingcardImgPath)

        

        await integration.response.send_message(embed=embed) """

        async def presentBJTable():
            options = ["🃏", "🛑"]
            firstMessage = f"{displayDeck(playerDeck, False)}Total: {getDeckSum(playerDeck)}\nDealer has {dealerDeck[0]} facing up\nDo you hit, stay, or surrender?"

            # Evaluate if the cards have same face value, present option to split if true
            if ((playerDeck[0][0:playerDeck[0].index("Of")] == playerDeck[1][0:playerDeck[1].index("Of")] or 
                (playerDeck[0][0:playerDeck[0].index("Of")] in faceCards and playerDeck[1][0:playerDeck[1].index("Of")] in faceCards)) and
                not deckSplit):
                options.append("🍌")
                firstMessage = firstMessage[0:firstMessage.index("or")-1] + " split, " + firstMessage[firstMessage.index("or"):]
            
            # Evaluate if the player has enough money to double down, present option if so
            if self.dbapi.currency.deduct(iid,"bot.currency", wager):
                # Possible bug here if program stops after condition check but before refund
                self.dbapi.currency.add(iid, "bot.currency", wager)
                options.append('⏬')
                firstMessage = firstMessage[0:firstMessage.index("or")-1] + " double down, " + firstMessage[firstMessage.index("or"):]

            # Evaluate if the dealer has an ace as their up-card, and offer the player insurance if so
            if dealerDeck[0][0:dealerDeck[0].index("Of")] == 'ace' and not insurancePlaced:
                options.append('💼')
                firstMessage = firstMessage[0:firstMessage.index("or")-1] + " buy insurace, " + firstMessage[firstMessage.index("or"):]
            
            options.append("🏳️")
            await integration.channel.send(firstMessage)
            # Should fix bug where first reaction would go on 2nd to last message
            # If there's a better way to target 'firstMessage' please tell me
            firstMessageObject = integration.channel.last_message

            # Present choices for player to make in the form of reactions
            for option in options:
                await firstMessageObject.add_reaction(option)

        def check(reaction: discord.Reaction, user: discord.User):
            if reaction.emoji in ['🃏', '🛑', '⏬', '💼', '🍌', '🏳️'] and not user.bot:
                return True
            return False
        
        async def getPlayerChoice():
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await integration.channel.send('👎')
            else:
                await integration.channel.send(reaction.emoji)
            return reaction.emoji
        
        # Main gameplay loop for the player
        inPlay = True
        while inPlay:
            await presentBJTable()
            playerChoice = await getPlayerChoice()
            if playerChoice == "🃏": # Player hits
                playerDeck.append(drawCard())
            elif playerChoice == "🛑": # Player stays
                inPlay = False
            elif playerChoice == "⏬": # Player Doubles Down
                self.dbapi.currency.deduct(iid,"bot.currency", wager)
                playerDeck.append(drawCard())
                inPlay = False
            elif playerChoice == "💼": # Player purchases insurance
                insurancePlaced = True
                # Bet of half of the wager, if possible
                if not self.dbapi.currency.deduct(iid, "bot.currency", int((0.5 * wager) + 0.5)):
                    await integration.channel.send('Not enough money to bet insurance!')
                # Dealer has blackjack, game ends
                elif dealerDeck[1][0:dealerDeck[1].index("Of")] in faceCards or dealerDeck[1][0:dealerDeck[1].index("Of")] == 'ten':
                    await integration.channel.send('Dealer has blackjack! Good call!')
                    self.dbapi.currency.add(iid, "bot.currency", wager)
                    inPlay = False
                    return None
                # Dealer does not have blackjack, losing the insurance bet
                else: # Note insurance bet has already been deducted
                    await integration.channel.send('No blackjack! Insurance bet lost.')
            elif playerChoice == "🍌": # Player splits hand
                # Split deck into two separate hands, and alternate between both hands
                # This will be a joy to program
                inPlay = False
            elif playerChoice == "🏳️": # Player surrenders
                self.dbapi.currency.add(iid, "bot.currency", int((0.5 * wager) + 0.5))
                inPlay = False
                await integration.channel.send('Understood, thanks for playing!')
                return None
            elif playerChoice == "👎": # Player does not choose in time
                await integration.channel.send('Too long to respond! Game over!')
                inPlay = False
            else:
                await integration.channel.send('Invalid choice! Please select from the choices provided.')

            # Player cannot split or place insurace after first round
            if not deckSplit:
                deckSplit = True
            
            if not insurancePlaced:
                insurancePlaced = True

            playerTotal = getDeckSum(playerDeck)

            if playerTotal == 21:
                await integration.channel.send(displayDeck(playerDeck, False) + "Total: " + str(playerTotal))
                await integration.channel.send('You have blackjack!')
                inPlay = False
            elif playerTotal > 21:
                await integration.channel.send(displayDeck(playerDeck, False) + "Total: " + str(playerTotal))
                await integration.channel.send('Over 21! You\'ve gone bust!')
                inPlay = False

        # Dealer gameplay algorithm
        dealerInPlay = True
        while dealerInPlay:
            dealerTotal = getDeckSum(dealerDeck)
            await integration.channel.send(displayDeck(dealerDeck, True) + "Total: " + str(dealerTotal))
            if dealerTotal > 21:
                await integration.channel.send('Dealer has gone bust!')
                dealerInPlay = False
            elif dealerTotal == 21:
                await integration.channel.send('Dealer has blackjack!')
                dealerInPlay = False
            elif 17 < dealerTotal < 21: # I'll figure out how to determine if it's a hard or soft 17 and adjust accordingly
                await integration.channel.send('Dealer stays!')
                dealerInPlay = False
            else:
                await integration.channel.send('Dealer hits!')
                dealerDeck.append(drawCard())
        
        # Determine the outcome of the game given the player's and dealer's hands
        gameOutcome = ''
        if dealerTotal > 21: # Player can get <= 21 or bust
            if playerTotal > 21:
                gameOutcome = 'Push'
            else:
                gameOutcome = 'Player'
        elif dealerTotal == 21: # Player either gets blackjack or loses otherwise
            if playerTotal == 21:
                gameOutcome = 'Push'
            else:
                gameOutcome = 'Dealer'
        else: # dealerTotal < 21
            if playerTotal > 21:
                gameOutcome = 'Dealer'
            elif playerTotal == 21:
                gameOutcome = 'Player'
            else:
                if playerTotal > dealerTotal:
                    gameOutcome = 'Player'
                elif playerTotal == dealerTotal:
                    gameOutcome = 'Push'
                else:
                    gameOutcome = 'Dealer'
        
        # Conclude the game and payout accordingly
        if gameOutcome == 'Dealer':
            await integration.channel.send('Dealer wins!')
        elif gameOutcome == 'Push':
            await integration.channel.send('Hand is a push!\nOriginal wager is returned.')
        elif gameOutcome == 'Player':
            await integration.channel.send(f'Player wins!\nPayout: {1.5 * wager}')
            self.dbapi.currency.add(iid, "bot.currency", int(1.5 * wager))
        else:
            await integration.channel.send(f'The devs didn\'t consider this scenario, please contact one about this game immediately!\nCourtesy Payout: {2 * wager}')
            self.dbapi.currency.add(iid, "bot.currency", int(2 * wager))
            
        await integration.channel.send('Thanks for playing!')


async def setup(bot):
    await bot.add_cog(Currency(bot,bot.dbapi))
