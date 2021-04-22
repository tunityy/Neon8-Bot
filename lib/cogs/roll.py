from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord import Embed, Member

from lib.dice.rolls import v5_roll


class Dice(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('Dice cog for bot is online.')


    ### COMMANDS ###


    @command(aliases=['basic', 'lite roll'], brief='Roll some dice! Total, Hunger, Successes Needed, Comments', description = """
    -------------------------
     FORMAT FOR ROLLING DICE
    -------------------------
    Example: .roll 5 2 3 Frenzy check (willpower + hum/3)

    <command> <total # of dice> <# of hunger dice> <successes needed> <Comments>

    Valid aliases to use this command are below in square brackets []. Beside that are the parameters.""")
    async def basicroll(self, ctx, dice_tot: int, dice_hunger: int, success_req: int, *args):
        rolled_stats = v5_roll(dice_tot, dice_hunger, success_req)
        dice_norm = int(dice_tot) - int(dice_hunger)

        stringified_comment = ' '.join(args)
        if stringified_comment == "":
            comment_final = ""
        else:
            comment_final = f"\n\nComment: *{stringified_comment}*"

        await ctx.send(f""" \u200b
   --- __**{ctx.author.display_name}**'s Roll__ ---
  *Normal dice: {dice_norm}, Hunger dice: {dice_hunger}*

**Result**:  __{rolled_stats[3]}__  [{rolled_stats[2]}]   *(Needed: {success_req})*
**Normal Dice**:  {rolled_stats[0]}
**Hunger Dice**:  {rolled_stats[1]} {rolled_stats[4]} {comment_final}""")



    @command(aliases=['rolldice', 'dice', 'v5', 'm5', 'v5roll', 'm5roll', 'r'], brief="Roll some dice! Total, Hunger, Successes Needed, Comments")
    async def roll(self, ctx, dice_tot: int, dice_hunger: int, success_req: int, *args):

        stringified_comment = ' '.join(args)
        if stringified_comment == "":
            comment_final = ""
        else:
            comment_final = f"\n\nComment: *{stringified_comment}*"

        embed = Embed(title = f"__{ctx.author.display_name}'s Roll__",
                      colour = discord.Colour.blue(),
                      timestamp = datetime.utcnow(),
                      description = f"{comment_final}")

        embed.set_thumbnail(url=ctx.author.avatar_url)
        # embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        if int(dice_tot) == 0:
            await ctx.send("""```
------------------------------------
 #### Error: You can't roll 0 dice!
------------------------------------```""")
        elif int(dice_hunger) > int(dice_tot): #I'm gonna have to change this once I make this based on a database :(
            await ctx.send("""```
--------------------------------------------------------------
 #### Error: You can't have more hunger dice than total dice!
--------------------------------------------------------------```""")
        else:
            rolled_stats = v5_roll(dice_tot, dice_hunger, success_req)
            dice_norm = int(dice_tot) - int(dice_hunger)

            fields = [("Result", f"{rolled_stats[3]}  [{rolled_stats[2]}]", False),
                    ("Normal Dice", f"{rolled_stats[0]}", True),
                    ("Hunger Dice", f"{rolled_stats[1]}", True)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)


    @command(aliases=['randroll', 'quantum', 'qr', 'quantumroll', 'quantum roll', 'truerandom'], brief='Roll some dice! Total, Hunger, Successes Needed, Comments', description = """
    -------------------------
     FORMAT FOR ROLLING DICE
    -------------------------
    Example: .roll 5 2 3 Frenzy check (willpower + hum/3)

    <command> <total # of dice> <# of hunger dice> <successes needed> <Comments>

    Valid aliases to use this command are below in square brackets []. Beside that are the parameters.""")
    async def qroll(self, ctx, dice_tot: int, dice_hunger: int, success_req: int, *args):

        rolled_stats = v5_roll(dice_tot, dice_hunger, success_req, True)
        dice_norm = int(dice_tot) - int(dice_hunger)

        stringified_comment = ' '.join(args)
        if stringified_comment == "":
            comment_final = ""
        else:
            comment_final = f"\n\nComment: *{stringified_comment}*"

        await ctx.send(f""" \u200b
   --- __**{ctx.author.display_name}**'s Roll__ --  ***Quantum Edition!***
  *Normal dice: {dice_norm}, Hunger dice: {dice_hunger}*

**Result**:  __{rolled_stats[3]}__  [{rolled_stats[2]}]   *(Needed: {success_req})*
**Normal Dice**:  {rolled_stats[0]}
**Hunger Dice**:  {rolled_stats[1]} {rolled_stats[4]} {comment_final}""")


def setup(client):
    client.add_cog(Dice(client))