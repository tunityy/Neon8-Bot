# from lib.db.db import stats_lookup, stats_lookup_list_all, name_lookup
# from lib.db.db import stat_name_ifs, column_to_text, stat_names_listifier
# from lib.db.db import update_stats, basic_listifier, update_character_name
# from lib.db.db import check_table_exists, increment, clear_stats

from lib.db.db import fregister_prompt, fregister_results, fsearch
from lib.db.db import query_user, _register, search, _list_all, _update, _increment, _reset, _delete_user

import sqlite3
import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, command, Greedy
from datetime import datetime

# TODO: Total overhaul of this cog, and all the associated functions. Working on it! :)

st_id = "put storyteller's userid number here"
owner_id = "put bot owner's userid number here"

def is_st_or_owner():
    async def pred(ctx):
        return ctx.author.id == owner_id or ctx.author.id == st_id
    return commands.check(pred)


class Stats(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('Stats cog for bot is online.')


    ### COMMANDS ###

    ### REGISTER PLAYER ###

    ## I have three options for register functions, all of which work. Need to decide what suits me best
    # TODO: add an error message for if a stat is misspelled?

#     @command(aliases = ['reg_basic', 'regplayer', 'regbasic', 'basicplayer', 'basicnew', 'newbasic'])
#     async def register_player(self, ctx, character_name=False):
#         my_result = query_user(ctx.author.id, ctx.guild.id)
#         if my_result is not None:
#             await ctx.send("Player is already registered in database.")

#         elif my_result is None:
#             result = _register(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, ())
#             await ctx.send(f"""Registered basic player information for **{ctx.author.display_name}** in database.
# No character stats have been added yet. Please use `.update` or `.set` to enter your stats.""")


    @command(name='register', aliases = ['reg', 'regnew', 'new'])
    async def register_new(self, ctx, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is not None:
            await ctx.send("Player is already registered in database.")
        elif my_result is None:
            print("\nRegister new")
            result = _register(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, args)
            if result == 'Invalid':
                await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower, health, superficial damage, aggravated damage.`""")
            elif result == ():
                await ctx.send(f"""**__{ctx.author.display_name}__**'s basic player information has been registered in the database.
No character stats have been added yet. Please use `.update` or `.set` to enter your stats.""")
            else:
                print(result)
                stats = fregister_results(result)
                print(stats)
                print()
                await ctx.send(f"""**__{ctx.author.display_name}__**'s player information has been registered, and the following stats have been set:\n{stats}""")
                # TODO: Add a degeneration check


    ## TODO: make some kind of error if it comes back as invalid
    @command(aliases=['regfull'])
    async def register_full(self, ctx):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is not None:
            await ctx.send("Player is already registered in database.")
        elif my_result is None:        
            await ctx.send("""Registering new character. Please provide, without brackets:
`(hunger), (humanity), (stains), (current willpower), (total willpower)`""")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.client.wait_for("message", check=check)
            rawinput = fregister_prompt(msg.content)
            result = _register(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, rawinput)
            # print(result)
            stats = fregister_results(result)
            await ctx.send(f"""**__{ctx.author.display_name}__**'s player information has been registered, and the following stats have been set:\n{stats}""")
            # TODO: Add a degeneration check?

    # ----------------------------------------------------------

    ### Lookup / Show / List ###

    @command(aliases=['see', 'view'])
    async def show(self, ctx, target: Greedy[Member], *args):
        if target == []:
            userID = ctx.author.id
            player = ctx.author # moved
        else:
            split_target = str(target).split(' ')
            ids = [x[3:] for x in split_target if x[0:3] == 'id=']
            userID = int(ids[0])
            player = ctx.author.guild.get_member(userID) #moved
        my_result = query_user(userID, ctx.guild.id)

        if my_result is None:
            await ctx.send("Player is not registered in database.")
        else:
            res = search(userID, ctx.author.guild.id, args)
            print(res)

            if res == 'Invalid':
                await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower, health, superficial damage, aggravated damage.`""")
            else:
                stats = fsearch(res)
                embed = Embed(title = f"__{player.display_name}'s Stats__",
                            colour = player.colour,
                            timestamp = datetime.utcnow(),
                            description = f"{stats}\n\u200b")
                            # colour=ctx.author.colour,
                            # colour = discord.Colour.purple(),
                embed.set_thumbnail(url=player.avatar_url)
                embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)


    @command(aliases=['showall', 'listall', 'list_all', 'list', 'seeall'])
    async def show_all(self, ctx, *args):
        res = _list_all(ctx.author.guild.id, args)
        if res == 'Invalid':
            await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower, health, superficial damage, aggravated damage.`""")
        else:
            column_names = res[0][18:]
            player_stats = [x[1:] for x in res[1]]
            player_names = [f"__{x[0]}__" for x in res[1]]

            result_list = [((column_names,), x) for x in player_stats]
            thingy = [fsearch(item) + "\n\u200b" for item in result_list]
            true_list = [True for x in player_names]
            lst = list(map(lambda x, y, z: (x, y, z), player_names, thingy, true_list))

            embed = Embed(title="List of Stats for All Players",
                        description="\u200b",
                        colour=ctx.author.colour,
                        timestamp=datetime.utcnow())

            embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

            fields = lst
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)
            # TODO: Make this look nicer?

    # ----------------------------------------------------------

    @command(aliases=['set', 'change'])
    async def update(self, ctx, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        invalid_msg = """Uh oh! I couldn't find that stat. Try one or more of the following:
`hunger, humanity, stains, current willpower, total willpower, health, superficial damage, aggravated damage`"""

        if my_result is None:
            result = _register(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, args)
            if result == 'Invalid':
                await ctx.send(invalid_msg)
                # This sends if the stat name was wrong AND/OR if the number isn't an integer value e.g. <3)>
                # So I may want to change the error message to reflect that it could be either of those

            elif result == ():
                await ctx.send(f"""**__{ctx.author.display_name}__**'s basic player information has been registered in the database.
No character stats have been added yet. Please use `.update` or `.set` to enter your stats.""")
            else:
                stats = fregister_results(result)
                await ctx.send(f"""**__{ctx.author.display_name}__**'s player information has been registered, and the following stats have been set:\n{stats}""")
            
        elif my_result is not None:
            res = _update(ctx.author.id, ctx.author.guild.id, args)
            if res == 'Invalid':
                await ctx.send(invalid_msg)
            else:
                stats = fregister_results(res)
                # TODO: maybe change it so it will show what the previous stat value was? E.g. Hunger updated from 2 to 3

                embed = Embed(title = f"__{ctx.author.display_name}'s Updated Stats__",
                            colour = ctx.author.colour,
                            timestamp = datetime.utcnow(),
                            description = f"{stats}\n\u200b")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                # TODO: Add a degeneration check


    @command(aliases=['updateother', 'set_other', 'setother', 'so'])
    async def update_other(self, ctx, target: Greedy[Member], *args):
        if target == []:
            await ctx.send("Error: No player was mentioned.")
        else:
            split_target = str(target).split(' ')
            ids = [x[3:] for x in split_target if x[0:3] == 'id=']
            userID = int(ids[0])
            if ctx.author.id == userID or ctx.author.id == owner_id or ctx.author.id == st_id:
                my_result = query_user(userID, ctx.guild.id)
                player = ctx.author.guild.get_member(userID)

                if my_result is None:
                    result = _register(player, player.display_name, userID, player.guild.id, args)
                    if result == ():
                        await ctx.send(f"""**__{player.display_name}__**'s basic player information has been registered in the database.
No character stats have been added yet. Please use `.update` or `.set` to enter your stats.""")
                    else:
                        stats = fregister_results(result)
                        await ctx.send(f"""**__{player.display_name}__**'s player information has been registered, and the following stats have been set:\n{stats}""")

                elif my_result is not None:   
                    res = _update(userID, player.guild.id, args)
                    if res == 'Invalid':
                        await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following:
`hunger, humanity, stains, current willpower, total willpower, health, superficial damage, aggravated damage.`""")
                    else:
                        stats = fregister_results(res)
                        # TODO: maybe change it so it will show what the previous stat value was? E.g. Hunger updated from 2 to 3

                        embed = Embed(title = f"__{player.display_name}'s Updated Stats__",
                                    colour = player.colour,
                                    timestamp = datetime.utcnow(),
                                    description = f"{stats}\n\u200b")
                        embed.set_thumbnail(url=player.avatar_url)
                        await ctx.send(embed=embed)
            else:
                await ctx.send("Error: User is not authorized to change other people's stats.")
            # TODO: Add a degeneration check


    # I don't even know if I'll keep this function
    # But the database stuff behind the scenes is really useful for auto-changing stats with dice rolls
    @command(aliases=['add'])
    async def plus(self, ctx, *args):
        ### TODO: make the output a little nicer, perhaps?
        res = _increment(ctx.author.id, ctx.author.guild.id, args)
        if res is None:
            await ctx.send("Player is not registered in database.")
        elif res == 'Invalid':
            await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower, health, superficial damage, aggravated damage.`""")
        else:
            if res[0] == res[1]:
                await ctx.send(f"{res[2]} remains unchanged at {res[1]}")
            if res[0] > res[1]:
                await ctx.send(f"Decreased {res[2]} from {res[0]} to {res[1]}.")
            if res[0] < res[1]:
                await ctx.send(f"Increased {res[2]} from {res[0]} to {res[1]}.")
            # TODO: Add a degeneration check

    # ----------------------------------------------------------

    # This command makes me nervous, even though I know that it's set up so only two people can use it
    @is_st_or_owner()
    @command(aliases = ['rem', 'del', 'delete'])
    async def remove(self, ctx, target: Greedy[Member]):
        if target == []:
            userID = ctx.author.id
            player = ctx.author
        else:
            split_target = str(target).split(' ')
            ids = [x[3:] for x in split_target if x[0:3] == 'id=']
            userID = int(ids[0])
            player = ctx.author.guild.get_member(userID)

        my_result = query_user(userID, ctx.guild.id)
        if my_result is None:
            await ctx.send("Player is not registered in database.")

        else:
            await ctx.send(f'''
This command will **permanently delete** __{player.display_name}__ from the database. This action cannot be undone.\n
Please confirm by typing "yes". Type anything else to cancel.''')
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.client.wait_for("message", check=check)
            confirmation = msg.content

            result = _delete_user(userID, ctx.guild.id, confirmation)

            if result == "Cancelled, user has not been deleted." or result[0] == "Cancelled, user has not been deleted.":
                await ctx.send(result)
            elif result == 'Something went wrong' or result[0] == 'Something went wrong':
                await ctx.send(result[0])
            else:
                await ctx.send(f"{player.display_name} has been successfully deleted.")

    # ----------------------------------------------------------


    @command(aliases=['stains', 'stian', 'st'])
    async def stain(self, ctx, number=1):

        res = _increment(ctx.author.id, ctx.author.guild.id, ('stains', str(number)))
        if res is None:
            await ctx.send("Player is not registered in database.")
        elif res == 'Invalid':
            await ctx.send("Something went wrong.")
        else:
            if res[0] == res[1]:
                await ctx.send(f"{res[2]} remains unchanged at {res[1]}")
            if res[0] > res[1]:
                await ctx.send(f"Decreased {res[2]} from {res[0]} to {res[1]}.")
            if res[0] < res[1]:
                await ctx.send(f"Increased {res[2]} from {res[0]} to {res[1]}.")
            # TODO: maybe make the output look a little nicer? Super low priority though
            # TODO: Add a degeneration check


    # ----------------------------------------------------------

#     ### CLEAR COMMAND GROUP ###

#     @commands.group(aliases = ['wipe'], invoke_without_command=True)
#     async def clear(self, ctx):
#         await ctx.send('''
# Available Clear Commands:
# clear my <stat>
# clear one <stat>
# clear all
# clear table
# ''')


#     @clear.command(name='my', aliases=['me'])
#     async def clear_my(self, ctx, *args):
#         # clears the stat for all your characters, or just one
#         my_result = query_user(ctx.author.id, ctx.guild.id)
#         if my_result is None:
#             await ctx.send("Player is not registered in database!")

#         elif my_result is not None and len(my_result) > 1:
#             await ctx.send(f"""Woops! It looks like you have more than one profile registered. You'll have to be more specific. 
# *(Note: this feature is under construction, and is not currently available.)*""")
#             # Eventually I'll have to modify this so it works for when you have more than one character...

#         else:
#             if args != () and stat_names_listifier(args) == 'Invalid':
#                 await ctx.send("""Error: invalid stat or stats. Please try one or more of the following:
# `hunger, humanity, stains, current willpower, total willpower`""")

#             else:
#                 if args == ():
#                     result = clear_stats(ctx.author.id, ctx.author.guild.id, args, True)
#                     cleared_msg = f"{ctx.author.display_name}'s stats have all been reset to 0."
#                 else:
#                     stats = stat_names_listifier(args)
#                     print(f"Stats: {stats}/, type: {type(stats)}/, len: {len(stats)}")
#                     result = clear_stats(ctx.author.id, ctx.author.guild.id, args)
#                     if type(stats) == str:
#                         cleared_msg = f"{ctx.author.display_name}'s {column_to_text(stats)} has been reset to 0."
#                     elif type(stats) == list and len(stats) == 2:
#                         column_list = [column_to_text(thing) for thing in stats]
#                         cleared_msg = f"{ctx.author.display_name}'s {column_list[0]} and {column_list[1]} have been reset to 0."
#                     elif type(stats) == list and len(stats) > 2:
#                         beginning_results = ', '.join(column_to_text(stats)[:-1])
#                         last_result = column_to_text(stats)[-1]
#                         cleared_msg == f"{ctx.author.display_name}'s {beginning_results}, and {last_result} have been reset to 0."
#                 print(result)
#                 if result == 'Cleared':
#                     await ctx.send(cleared_msg)
#                 else:
#                     await ctx.send("Oops, something went wrong.")


#     @clear.command(name='one', aliases=['other'])
#     async def clear_one(self, ctx, member: Member, *args):
#         search_res = query_user(ctx.author.id, ctx.guild.id)
#         if search_res is None:
#             await ctx.send(f"{member.display_name} could not be found in the database. :(")

#         elif search_res is not None and len(search_res) > 1:
#             await ctx.send(f"""Woops! It looks like there's more than one profile registered to that player. You'll have to be more specific. 
# *(Note: this feature is under construction, and is not currently available.)*""")
#             # Eventually I'll have to modify this so it works for when you have more than one character...            

#         else:
#             if args != () and stat_names_listifier(args) == 'Invalid':
#                 await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
# `hunger, humanity, stains, current willpower, total willpower.`""")

#             else:
#                 if args == ():
#                     result = clear_stats(member.id, ctx.author.guild.id, args, True)
#                     cleared_msg = f"{member.mention}'s stats have all been reset to 0."
#                 else:
#                     stats = stat_names_listifier(args)
#                     print(f"Stats: {stats}/, type: {type(stats)}/, len: {len(stats)}")
#                     result = clear_stats(member.id, ctx.author.guild.id, args)
#                     if type(stats) == str:
#                         cleared_msg = f"{member.mention}'s {column_to_text(stats)} has been reset to 0."
#                     elif type(stats) == list and len(stats) == 2:
#                         column_list = [column_to_text(thing) for thing in stats]
#                         cleared_msg = f"{member.mention}'s {column_list[0]} and {column_list[1]} have been reset to 0."
#                     elif type(stats) == list and len(stats) > 2:
#                         beginning_results = ', '.join(column_to_text(stats)[:-1])
#                         last_result = column_to_text(stats)[-1]
#                         cleared_msg == f"{member.mention}'s {beginning_results}, and {last_result} have been reset to 0."
#                 print(result)
#                 if result == 'Cleared':
#                     await ctx.send(cleared_msg)
#                 else:
#                     await ctx.send("Oops, something went wrong.")


#     @clear.command(name='all', aliases=['everyone'])
#     async def clear_all(self, ctx):
#         await ctx.send("This is a generic message, to use as an example.")
#         # clears the stat for all players in guild


#     @clear.command(name='table', aliases=['clean_slate'])
#     async def clear_table(self, ctx):
#         await ctx.send("This is a generic message, to use as an example.")
#         # deletes all rows in that table. There will be a default for dynamic_stats, but you can write a table name to make the command more useful in future


#     # ----------------------------------------------------------

def setup(client):
    client.add_cog(Stats(client))
