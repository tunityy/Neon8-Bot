from lib.db.db import query_player, player_info, register
from lib.db.db import stats_lookup, stats_lookup_list_all
from lib.db.db import stat_name_ifs, column_to_text, stat_names_listifier
from lib.db.db import update_stats, basic_listifier

import sqlite3
import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, command
from datetime import datetime



class Stats(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('Stats cog for bot is online.')


    ### COMMANDS ###

    @command()
    async def generic(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")


    ### Lookup / Show / List ###

    # This is an example of what I'd like the end result to be like, more or less.
    # I'm gonna format it a bit more to make it prettier. :P
    @command(aliases=['showmethemoney'])
    async def money(self, ctx, *args):
        print("\n-------------Start")

        embed = Embed(title="Here are some results I guess",
                      description="Oh dear.",
                      colour=ctx.author.colour,
                      timestamp=datetime.utcnow())

        embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        fields = [('Health', 'Markus: 1 \nLio: 5 \nRagemar: 9', True),
                  ('Hunger', 'Markus: 2 \nLio: 6 \nRagemar: 10', True),
                  ('Stains', 'Markus: 3 \nLio: 7 \nRagemar: 11', True),
                  ('Current Willpower', 'Markus: 4 \nLio: 8 \nRagemar: 12', True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)



    # My initial attempt for a listall command, with results grouped by player
    @command(aliases=['showall', 'lookall', 'list', 'listall', 'show_all', 'look_all'])
    async def list_all(self, ctx, *args):
        print("\n-------------Start")
        if args == ():
            search_res = stats_lookup_list_all(ctx.author.id, ctx.author.guild.id, args, True)
        else:
            search_res = stats_lookup_list_all(ctx.author.id, ctx.author.guild.id, args)
        stat_names = [column_to_text(x) for x in search_res[0]]
        player_raw_results = search_res[1]

        player_names = [player[0] for player in player_raw_results]
        raw_numbers = [x[1:] for x in player_raw_results]
        str_numbs = [[str(x) for x in tup] for tup in raw_numbers]

        named_stats = [list(zip(stat_names, thing)) for thing in str_numbs]
        add_colons = [[': '.join(x) for x in y] for y in named_stats]
        stat_list_thing = [('\n'.join(thing)) for thing in add_colons]

        l0 = player_names
        l1 = stat_list_thing
        l2 = [True for x in player_names]
        lst = list(map(lambda x, y, z: (x, y, z), l0, l1, l2))

        embed = Embed(title="Here are some results I guess",
                      description="Oh dear.",
                      colour=ctx.author.colour,
                      timestamp=datetime.utcnow())

        if ctx.author.nick is None:
            embed.set_footer(text=f"Requested by:  {ctx.author.name}", icon_url=ctx.author.avatar_url)
        else:
            embed.set_footer(text=f"Requested by:  {ctx.author.nick}", icon_url=ctx.author.avatar_url)

        fields = lst
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

        print("")



    # Returns results for the person putting in the command
    @command(aliases=['showme', 'look', 'show'])
    async def show_me(self, ctx, *args):
        my_result = query_player(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send("Player is not registered in database!")
        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"Woops! It looks like there's more than one profile registered to that player. You'll have to be more specific.")

        elif my_result is not None and len(my_result) == 1:
            search_res = stats_lookup(ctx.author.id, ctx.author.guild.id, args)

            stat_names = [column_to_text(x) for x in search_res[0]]
            nums_strings = [str(thing) for thing in search_res[1]]
            pairs = tuple(zip(stat_names, nums_strings))
            output = ', '.join([': '.join(pair) for pair in pairs])

            await ctx.send(f"Search results: {output}")


    # Returns results for the person you @mention
    @command(aliases=['showone', 'showyou', 'lookone', 'look_one', 'show_other'])
    async def show_one(self, ctx, member: Member, *args):
        my_result = query_player(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send(f"{member.display_name} could not be found in the database. :(")
        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"Woops! It looks like there's more than one profile registered to that player. You'll have to be more specific.")

        elif my_result is not None and len(my_result) == 1:
            print("")
            search_res = stats_lookup(member.id, ctx.author.guild.id, args, False)
            # print(search_res)

            if search_res is None:
                await ctx.send(f"{member.display_name} could not be found in the database. :(")

            else:
                stat_names = [column_to_text(x) for x in search_res[0]]
                nums_strings = [str(thing) for thing in search_res[1]]

                if len(stat_names) == 1:
                    await ctx.send(f"{member.mention}'s {stat_names[0]} is {nums_strings[0]}")
                else:
                    pairs = tuple(zip(stat_names, nums_strings))
                    output = '\n'.join([': '.join(pair) for pair in pairs])

                    await ctx.send(f"Inquiry for {member.mention}'s stats: \n{output}")



    # I have additional commands coded for registering a player or character, and updating your stats.
    # But I didn't include them because they're not really relevant.
    # Maybe they are though, so let me know.


def setup(client):
    client.add_cog(Stats(client))
