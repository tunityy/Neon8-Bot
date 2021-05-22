from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord import Embed, Member

from lib.dice.checks import dice_checks
from lib.dice.rolls import v5_roll
from lib.db.db import extra_spacing as es
from lib.db.db import db_select


class Dice(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('Dice cog for bot is online.')


    ### COMMANDS ###


    @command(aliases=['basic', 'br'], brief='Roll some dice! Total, Hunger, Successes Needed, Comments', description = """
    -------------------------
     FORMAT FOR ROLLING DICE
    -------------------------
    Example: .basicroll 5 2 3 Frenzy check (willpower + hum/3)

    <command> <total # of dice> <# of hunger dice> <successes needed> <Comments>""")
    async def basicroll(self, ctx, dice_tot: int, dice_hunger, success_req: int, *args):
        res = dice_checks(dice_tot, dice_hunger, ctx.author.id, ctx.author.guild.id, ctx.author, ctx.author.display_name)
        if res[0] == False:
            await ctx.send(res[1])
        elif res[0] != False:
            if len(res) == 2:
                dice_hunger = res[1]
                new_player = False
            elif len(res) == 3:
                new_player = res[1]
                dice_hunger = res[2]

            rolled_stats = v5_roll(dice_tot, dice_hunger, success_req)
            dice_norm = int(dice_tot) - int(dice_hunger)

            stringified_comment = ' '.join(args)
            if stringified_comment == "":
                comment_final = ""
            else:
                comment_final = f"\n\nComment: *{stringified_comment}*"
            
            if new_player is not False:
                comment_final = comment_final + f"\n\*\* {new_player}"
                dice_hunger = f"{dice_hunger}\*\*"

            await ctx.send(f""" \u200b
   --- __**{ctx.author.display_name}**'s Roll__ ---
  *Normal dice: {dice_norm}, Hunger dice: {dice_hunger}*

**Result**:  __{rolled_stats[3]}__  [{rolled_stats[2]}]   *(Needed: {success_req})*
**Normal Dice**:  {rolled_stats[0]}
**Hunger Dice**:  {rolled_stats[1]} {rolled_stats[4]} {comment_final}""")


    @command(aliases=['r', 'v5', 'm5', 'v5roll', 'm5roll', 'roll5e', 'rollv5'], brief="Roll some dice! Total, Hunger, Successes Needed, Comments")
    async def roll(self, ctx, dice_tot: int, dice_hunger, success_req: int, *args):
        res = dice_checks(dice_tot, dice_hunger, ctx.author.id, ctx.author.guild.id, ctx.author, ctx.author.display_name)
        if res[0] == False:
            await ctx.send(res[1])
        elif res[0] != False:
            if len(res) == 2:
                dice_hunger = res[1]
                new_player = False
            elif len(res) == 3:
                new_player = res[1]
                dice_hunger = res[2]

            rolled_stats = v5_roll(dice_tot, dice_hunger, success_req)
            dice_norm = int(dice_tot) - int(dice_hunger)

            stringified_comment = ' '.join(args)
            if stringified_comment == "":
                comment_final = ""
            else:
                comment_final = f"\n\nComment: *{stringified_comment}*"
            
            if new_player is not False:
                comment_final = f"\*\* {new_player}" + comment_final
                # comment_final = comment_final + f"\n\n\*\* {new_player}"
                dice_hunger = f"{dice_hunger}\*\*"

            embed = Embed(title = f"__{ctx.author.display_name}'s Roll__",
                        colour = discord.Colour.blue(),
                        timestamp = datetime.utcnow(),
                        description = f"{comment_final}")
            embed.set_thumbnail(url=ctx.author.avatar_url)

            if rolled_stats[3][-1] == '*':
                success = f"__{rolled_stats[3][:-2]}__\*"
            else:
                success = f"__{rolled_stats[3]}__"

            fields = [(f"{es(3)} Result", f"{es(3)} {success} {es(1)} [{rolled_stats[2]}]", True),#\n*Needed: {success_req}*", True),
                      ("\u200b", f"*{es(3)} Needed: {success_req}*", True),
                      ("\u200b", "\u200b", True),
                      (f"{es(3)} Normal Dice", f"{es(3)} {rolled_stats[0]}", True),
                      (f"{es(3)} Hunger Dice", f"{es(3)} {rolled_stats[1]}", True),
                      ("\u200b", "\u200b", True)]
            #         # TODO: change formatting so it matches basic_roll re: Successes Needed

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)


            # Below is commented out because I'm experimenting with formatting the output

            # if rolled_stats[3][-1] == '*':
            #     success = f"{rolled_stats[3][:-2]}\*"
            # else:
            #     success = f"{rolled_stats[3]}"

            # fields = [("Result", f"{success} {es(2)} [{rolled_stats[1]}]\n\n**Normal Dice** {es(1)} ({dice_norm})\n{rolled_stats[0]}", True),
            #           ("\u200b", f"*Needed: {success_req}*\n\n**Hunger Dice** {es(1)} ({dice_hunger})\n{rolled_stats[1]}", True)]
            #         #   ("\u200b", "\u200b", False),
            #         #   (f"Normal Dice {es(1)} ({dice_norm})", f"{rolled_stats[0]}", True),
            #         #   (f"Hunger Dice {es(1)} ({dice_hunger})", f"{rolled_stats[1]}", True)]



    @command(aliases=['randroll', 'qr', 'quantum', 'random'], brief='Roll some dice! Total, Hunger, Successes Needed, Comments', description = """
    -------------------------
     FORMAT FOR ROLLING DICE
    -------------------------
    Example: .qroll 5 2 3 Frenzy check (willpower + hum/3)

    <command> <total # of dice> <# of hunger dice> <successes needed> <Comments>""")
    async def qroll(self, ctx, dice_tot: int, dice_hunger, success_req: int, *args):
        res = dice_checks(dice_tot, dice_hunger, ctx.author.id, ctx.author.guild.id, ctx.author, ctx.author.display_name)
        if res[0] == False:
            await ctx.send(res[1])
        elif res[0] != False:
            await ctx.send("Consulting the quantum void...", delete_after=2)
            if len(res) == 2:
                dice_hunger = res[1]
                new_player = False
            elif len(res) == 3:
                new_player = res[1]
                dice_hunger = res[2]

            async with ctx.channel.typing():
                rolled_stats = v5_roll(dice_tot, dice_hunger, success_req, True)
                dice_norm = int(dice_tot) - int(dice_hunger)

                stringified_comment = ' '.join(args)
                if stringified_comment == "":
                    comment_final = ""
                else:
                    comment_final = f"\n\nComment: *{stringified_comment}*"
                
                if new_player is not False:
                    comment_final = comment_final + f"\n\*\* {new_player}"
                    dice_hunger = f"{dice_hunger}\*\*"

            await ctx.send(f""" \u200b
   --- __**{ctx.author.display_name}**'s Roll__ --  ***Quantum Edition!***
  *Normal dice: {dice_norm}, Hunger dice: {dice_hunger}*

**Result**:  __{rolled_stats[3]}__  [{rolled_stats[2]}]   *(Needed: {success_req})*
**Normal Dice**:  {rolled_stats[0]}
**Hunger Dice**:  {rolled_stats[1]} {rolled_stats[4]} {comment_final}""")


def setup(client):
    client.add_cog(Dice(client))