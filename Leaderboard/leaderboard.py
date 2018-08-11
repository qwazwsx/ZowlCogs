import discord
from discord.ext import commands
from discord import client
from redbot.core import Config, bank
#from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import asyncio

class Leaderboard:



    def __init__(self, bot):
        print('Loaded Leaderboard')
        self.tasks = []
        self.last_leaderboard = None
        self.bot = bot

        self.channel = self.bot.get_channel(474332690381013002)

        for message in self.channel.history(limit=5):
            if message.author.id == 474030873742671892:
                self.leaderboard_message = message
                break
        else:
            self.leaderboard_message = channel.send('Loading leaderboard...')

        #self.tasks.append(self.bot.loop.create_task(self.update_leaderboard()))

    def __unload(self):
        for task in self.tasks:
            task.cancel()
            print('Canceled')


    @commands.command()
    async def ul(self, ctx):

        self.tasks.append(await self.bot.loop.create_task(self.update_leaderboard(ctx)))



    """
    updates the leaderboard by either making a new message if none exists or editing an existing ones

    original function taken and modified from redbot/cogs/bank

    """
    #@commands.command()
    async def update_leaderboard(self, ctx: commands.Context = None, top: int = 10, show_global: bool = False):
        while True:
        
            ctx = self.leaderboard_message

            guild = ctx.guild
            author = ctx.author
            if top < 1:
                top = 10
            if (
                await bank.is_global() and show_global
            ):  # show_global is only applicable if bank is global
                guild = None
            bank_sorted = await bank.get_leaderboard(positions=top, guild=guild)
            if len(bank_sorted) < top:
                top = len(bank_sorted)
            header = f"{f'#':4}{f'Name':36}{f'Score':2}\n"
            highscores = [
                (
                    f"{f'{pos}.': <{3 if pos < 10 else 2}} {acc[1]['name']: <{35}s} "
                    f"{acc[1]['balance']: >{2 if pos < 10 else 1}}\n"
                )
                for pos, acc in enumerate(bank_sorted, 1)
            ]
            if highscores:
                pages = [
                    f"```md\n{header}{''.join(''.join(highscores[x:x + 10]))}```"
                    for x in range(0, len(highscores), 10)
                ]

                if self.last_leaderboard != pages[0]:
                    self.last_leaderboard = pages[0]

                    if self.leaderboard_message == None:
                        await self.channel.send(pages[0])
                    else:
                        try: 
                            await self.leaderboard_message.edit(content=str(pages[0]))
                        except HTTPException:
                            await self.leaderboard_message.delete()
                            await self.channel.send(pages[0])

            else:
                pass
                #await ctx.send("There are no accounts in the bank.")


            await asyncio.sleep(6)

        print('out')




