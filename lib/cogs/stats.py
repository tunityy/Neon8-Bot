from lib.db.db import query_user, player_info, register, register_variable#, query_player
from lib.db.db import stats_lookup, stats_lookup_list_all, name_lookup
from lib.db.db import stat_name_ifs, column_to_text, stat_names_listifier
from lib.db.db import update_stats, basic_listifier, update_character_name
from lib.db.db import check_table_exists, increment, clear_stats

import sqlite3
import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, command
from datetime import datetime

# TODO: Total overhaul of this cog, and all the associated functions. Working on it! :)


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


    # ----------------------------------------------------------

    ### REGISTER PLAYER ###

    @command(aliases = ['reg_basic', 'regplayer', 'regbasic', 'basicplayer', 'basicnew', 'newbasic'])
    async def register_player(self, ctx, character_name=False):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is not None:
            await ctx.send("Player is already registered in database.")

        elif my_result is None:
            my_info = player_info(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id)
            register(my_info, character_name)
            await ctx.send(f"""Registered basic player information for **{ctx.author.display_name}** in database.
\nNo character stats have been added yet. Please use `.update` or `.set` to enter your stats.""")


#     @command(aliases = ['reg_full', 'regfull', 'fullreg', 'register', 'registerfull', 'newplayer', 'fullnew', 'newfull', 'reg'])
#     async def register_full(self, ctx):
#         my_result = query_user(ctx.author.id, ctx.guild.id)
#         if my_result is not None:
#             await ctx.send("Player is already registered in database.")

#         elif my_result is None:
#             await ctx.send("""Registering new character. Please provide, without brackets:\n
# (current hunger), (current humanity), (stains), (current willpower), (total willpower)""")
#             ### Though character isn't referenced here, you can enter a separate character name

#             def check(msg):
#                 return msg.author == ctx.author and msg.channel == ctx.channel
#             msg = await self.client.wait_for("message", check=check)

#             # char_info = list(str(msg.content).replace(' ', ', ').split(', '))
#             char_info = basic_listifier(msg.content)

#             if len(char_info) != 5 and len(char_info) != 6:
#                 await ctx.send("Incorrect number of values entered!")
#             else:
#                 if len(char_info) == 5:
#                     character_name = False
#                     char_stats = char_info
#                 elif len(char_info) == 6:
#                     character_name = char_info[0]
#                     char_stats = char_info[1:6] 

#                 my_info = player_info(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id)
#                 register(my_info, character_name, True, char_stats)
            
#                 print(f"\nEntry for {msg.author.display_name}'s new character has been created.")
#                 await ctx.send(f"Character information for {msg.author.display_name} has been saved to database.")

    # ----------------------------------------------------------

    ### Lookup / Show / List ###


    @command(aliases=['showme', 'look', 'show'])
    async def show_me(self, ctx, *args):
        print(args)
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send("Player is not registered in database!")
        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"Woops! It looks like there's more than one profile registered to that player. You'll have to be more specific. \n(Note: this feature is under construction.)")
            # TODO: Make it work with more than one character per player

        elif my_result is not None and len(my_result) == 1:
            if args == ():
                search_res = stats_lookup(ctx.author.id, ctx.guild.id, args, True)
            else:
                search_res = stats_lookup(ctx.author.id, ctx.author.guild.id, args)

            if search_res == 'Invalid':
                await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower.`""")
            else:
                stat_names = [column_to_text(x) for x in search_res[0]]
                nums_strings = [str(i) for i in search_res[1]]

                if len(stat_names) == 1:
                    await ctx.send(f"{ctx.author.display_name}'s {stat_names[0]} is {nums_strings[0]}")
                else:
                    pairs = tuple(zip(stat_names, nums_strings))

                    # output = ', '.join([': '.join(pair) for pair in pairs])
                    output = '\n'.join([': '.join(pair) for pair in pairs])
                    await ctx.send(f"{ctx.author.display_name}'s stats: \n{output}")
                    # TODO: pretty up the message


    @command(aliases=['showone', 'showyou', 'lookone', 'look_one', 'show_other', 'showother'])
    async def show_one(self, ctx, member: Member, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send(f"{member.display_name} could not be found in the database. :(")
        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"""Woops! It looks like there's more than one profile registered to that player. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")

        elif my_result is not None and len(my_result) == 1:
            if args == ():
                search_res = stats_lookup(member.id, ctx.guild.id, args, True)
            else:
                search_res = stats_lookup(member.id, ctx.author.guild.id, args)

            if search_res == 'Invalid':
                await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower.`""")
            else:
                stat_names = [column_to_text(x) for x in search_res[0]]
                nums_strings = [str(i) for i in search_res[1]]

                if len(stat_names) == 1:
                    await ctx.send(f"{member.mention}'s {stat_names[0]} is {nums_strings[0]}")
                else:
                    pairs = tuple(zip(stat_names, nums_strings))

                    # output = ', '.join([': '.join(pair) for pair in pairs])
                    output = '\n'.join([': '.join(pair) for pair in pairs])
                    await ctx.send(f"Inquiry for {member.mention}'s stats: \n{output}")
                    # TODO: pretty up the message


    # TODO: Actually make this command work and look good, lol
    @command(aliases=['showall', 'lookall', 'list', 'listall', 'show_all', 'look_all'])
    async def list_all(self, ctx, *args):
        # print("\n-------------Start")
        if args == ():
            search_res = stats_lookup_list_all(ctx.author.id, ctx.author.guild.id, args, True)
        else:
            search_res = stats_lookup_list_all(ctx.author.id, ctx.author.guild.id, args)

        stat_names = [column_to_text(x) for x in search_res[0]]
        player_raw_results = search_res[1]

        player_names = [player[0] for player in player_raw_results]
        raw_numbers = [x[1:] for x in player_raw_results]
        str_numbs = [[str(x) for x in tup] for tup in raw_numbers]

        ### LIST BY STAT ###
        # add_colons = [x + ": " for x in player_names]
        # name_list = [[add_colons[i] + str_numbs[i][j] for j in range(len(str_numbs[0]))] for i in range(len(add_colons))]
        # grouped_by_stat = [[name_list[i][j] for i in range(len(name_list))] for j in range(len(stat_names))]
        # newLine_names = [('\n'.join(i)) for i in grouped_by_stat]
        # l0 = stat_names
        # l1 = newLine_names
        # l2 = [True for x in stat_names]

        ### LIST BY PLAYER ###
        named_stats = [list(zip(stat_names, x)) for x in str_numbs]
        add_colons = [[': '.join(x) for x in y] for y in named_stats]
        stat_list_thing = [('\n'.join(i)) for i in add_colons]
        l0 = player_names
        l1 = stat_list_thing
        l2 = [True for x in player_names]

        lst = list(map(lambda x, y, z: (x, y, z), l0, l1, l2))

        embed = Embed(title="Here are some results I guess",
                      description="Oh dear.",
                      colour=ctx.author.colour,
                      timestamp=datetime.utcnow())

        embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        fields = lst
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)
        # TODO: Make this look nice

    # ----------------------------------------------------------

    ### Update/Set My / One / All ###
    # TODO: Make a command to set someone else's stats

    @command(aliases=['set', 'setmy', 'set_my', 'updatemy', 'update_my'])
    async def update(self, ctx, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)

        print("\n----- Start -----")
        my_info = player_info(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id)
        print(my_info)
        print(type(my_info))
        print(ctx.author)
        print(f"{ctx.author}")
        print(type(ctx.author))
        print()

        if my_result is not None and len(my_result) > 1:
            await ctx.send(f"""Woops! It looks like you have more than one profile registered. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")            
            # Eventually I'll have to modify this so it works for when you have more than one character...

        else:
            listified_args = stat_names_listifier(args, True)
            if listified_args == 'Invalid':
                await ctx.send("""Error: invalid stat and/or value. Please use this format to update your stats: `.update stains 1, hunger 2`

These are the stats that are currently implemented in the database:
`hunger, humanity, stains, current willpower, total willpower`""")

            else:
                if my_result is None:
                    my_info = player_info(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id)
                    register_new = register_variable(my_info, args)

                    if len(register_new[1]) == 1:
                        stat_name = column_to_text(register_new[0])
                        await ctx.send(f"Added {ctx.author.display_name} to database and set {stat_name} to {register_new[1][0]}.")

                    else:
                        combined_results = list(map(lambda x, y: (x, y), basic_listifier([column_to_text(i) for i in register_new[0]]), register_new[1]))
                        final_output = ', '.join([f"{item[0]} to {item[1]}" for item in combined_results[:-1]])
                        last_result = [f"{item[0]} to {item[1]}" for item in [combined_results[-1]]]

                        if len(register_new[0]) == 1:
                            await ctx.send(f"Added {ctx.author.display_name} to database and set {final_output} and {last_result}")
                        else:
                            await ctx.send(f"Added {ctx.author.display_name} to database and set {final_output}, and {last_result[0]}")
                            # TODO: pretty up the message

                elif my_result is not None and len(my_result) == 1:
                    if isinstance(listified_args[0], str):
                        lookup_input = (listified_args[0],) 
                    elif len(listified_args[0]) > 1:
                        lookup_input = ',, '.join(listified_args[0]).split(', ')

                    before = stats_lookup(ctx.author.id, ctx.author.guild.id, lookup_input)
                    after = update_stats(ctx.author.id, ctx.author.guild.id, args)
                    
                    print("\nArgs")
                    print(args)
                    print(type(args))
                    print(f"Lookup input: {lookup_input}/, type: {type(lookup_input)}")
                    print(f"Lookup input 0: {lookup_input[0]}/, type: {type(lookup_input[0])}")
                    print()
                    print(before)
                    print(after)
                    print()
                    

                    if len(after[1]) == 1:
                        await ctx.send(f"Updated {column_to_text(lookup_input[0])} from {before[1][0]} to {after[1][0]}.")
                        print("column_to_text stuff")
                        print(column_to_text(lookup_input[0]))
                    else:
                        combined_results = list(map(lambda x, y, z: (x, y, z), basic_listifier([column_to_text(i) for i in lookup_input]), before[1], after[1]))
                        final_output = '\n'.join([f"Updated {item[0]} from {item[1]} to {item[2]}." for item in combined_results])                    
                        await ctx.send(f"{final_output}")
                        print(combined_results)
                        print(final_output)
                        # TODO: pretty up the message
                    print("----- End -----\n")



    @command(aliases=['change_name', 'updatename', 'changename', 'rename', 'setname', 'set_name'])
    async def update_name(self, ctx, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send(f"{ctx.author.display_name} could not be found in the database. :(")
            
        elif my_result is not None and len(my_result) > 1:

            await ctx.send(f"""Woops! It looks like you have more than one profile registered. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")
            # TODO: have to modify this so it works for when you have more than one character...

        elif my_result is not None and len(my_result) == 1:
            before = name_lookup(ctx.author.id, ctx.author.guild.id)
            update = update_character_name(ctx.author.id, ctx.author.guild.id, [' '.join(args)])

            await ctx.send(f"{ctx.author.display_name}'s character name has been changed from *{before[0]}* to **{update[0]}**")
            # TODO: Make this look a bit nicer maybe?


    # TODO: make this have an actual output of some kind in discord, lmao
    @command(aliases=['setall', 'updateall', 'set_all'])
    async def update_all(self, ctx, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is None:
            # TODO: make this prompt the user to add all their info and register
            await ctx.send("Player is not registered in database.")

        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"""Woops! It looks like you have more than one profile registered. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")
            # TODO: have to modify this so it works for when you have more than one character...

        elif my_result is not None and len(my_result) == 1:
            await ctx.send("""Updating all stats. Please provide, without brackets:\n
(current hunger), (current humanity), (stains), (current willpower), (total willpower)""")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.client.wait_for("message", check=check)

            char_info = basic_listifier(msg.content)

            if len(char_info) != 5 and len(char_info) != 6:
                await ctx.send("Incorrect number of values entered!")
            else:
                if len(char_info) == 5:
                    character_name = False
                    char_stats = char_info
                elif len(char_info) == 6:
                    character_name = char_info[0]
                    char_stats = char_info[1:6]

                before = stats_lookup(ctx.author.id, ctx.author.guild.id, args, True)
                after = update_stats(ctx.author.id, ctx.author.guild.id, char_stats, True, character_name)
                before_numbs = list(before[1])
                after_numbs = list(after[1])

                await ctx.send(f"""__Updated stats__
Hunger: {after_numbs[0]} (was {before_numbs[0]})
Humanity: {after_numbs[1]} (was {before_numbs[1]})
Stains: {after_numbs[2]} (was {before_numbs[2]})
Current Willpower: {after_numbs[3]} (was {before_numbs[3]})
Total Willpower: {after_numbs[4]} (was {before_numbs[4]})
""")


    @command(aliases=['plus', 'increase'])
    async def add(self, ctx, *args):
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send("Player is not registered in database!")

        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"""Woops! It looks like you have more than one profile registered. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")
            # Eventually I'll have to modify this so it works for when you have more than one character...

        else:
            raw_info = stat_names_listifier(args, True)
            if raw_info == 'Invalid':
                stat = stat_names_listifier(args)
                increase_by = 1
            else:
                stat = raw_info[0]
                increase_by = raw_info[1][0]
            if stat == 'Invalid':
                await ctx.send("Oops, something went wrong.")
            elif type(stat) == list:
                await ctx.send("Sorry, I can only increase one stat at a time with this command right now.")
            else:
                before = stats_lookup(ctx.author.id, ctx.author.guild.id, basic_listifier(stat))
                after = increment(ctx.author.id, ctx.author.guild.id, stat, increase_by)
                stat_name = column_to_text(before[0][0])

                before_numb = int(before[1][0])
                after_numb = int(after[0])

                if before_numb < after_numb:
                    await ctx.send(f"Increased {stat_name} from {before_numb} to {after_numb}.")
                elif before_numb > after_numb:
                    await ctx.send(f"Decreased {stat_name} from {before_numb} to {after_numb}.")
                elif before_numb == after_numb:
                    await ctx.send(f"{stat_name} remains unchanged at {after_numb}")

    # ----------------------------------------------------------

    ### CLEAR COMMAND GROUP ###

    @commands.group(aliases = ['wipe'], invoke_without_command=True)
    async def clear(self, ctx):
        await ctx.send('''
Available Clear Commands:
clear my <stat>
clear one <stat>
clear all
clear table
''')


    @clear.command(name='my', aliases=['me'])
    async def clear_my(self, ctx, *args):
        # clears the stat for all your characters, or just one
        my_result = query_user(ctx.author.id, ctx.guild.id)
        if my_result is None:
            await ctx.send("Player is not registered in database!")

        elif my_result is not None and len(my_result) > 1:
            await ctx.send(f"""Woops! It looks like you have more than one profile registered. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")
            # Eventually I'll have to modify this so it works for when you have more than one character...

        else:
            if args != () and stat_names_listifier(args) == 'Invalid':
                await ctx.send("""Error: invalid stat or stats. Please try one or more of the following:
`hunger, humanity, stains, current willpower, total willpower`""")

            else:
                if args == ():
                    result = clear_stats(ctx.author.id, ctx.author.guild.id, args, True)
                    cleared_msg = f"{ctx.author.display_name}'s stats have all been reset to 0."
                else:
                    stats = stat_names_listifier(args)
                    print(f"Stats: {stats}/, type: {type(stats)}/, len: {len(stats)}")
                    result = clear_stats(ctx.author.id, ctx.author.guild.id, args)
                    if type(stats) == str:
                        cleared_msg = f"{ctx.author.display_name}'s {column_to_text(stats)} has been reset to 0."
                    elif type(stats) == list and len(stats) == 2:
                        column_list = [column_to_text(thing) for thing in stats]
                        cleared_msg = f"{ctx.author.display_name}'s {column_list[0]} and {column_list[1]} have been reset to 0."
                    elif type(stats) == list and len(stats) > 2:
                        beginning_results = ', '.join(column_to_text(stats)[:-1])
                        last_result = column_to_text(stats)[-1]
                        cleared_msg == f"{ctx.author.display_name}'s {beginning_results}, and {last_result} have been reset to 0."
                print(result)
                if result == 'Cleared':
                    await ctx.send(cleared_msg)
                else:
                    await ctx.send("Oops, something went wrong.")


    @clear.command(name='one', aliases=['other'])
    async def clear_one(self, ctx, member: Member, *args):
        search_res = query_user(ctx.author.id, ctx.guild.id)
        if search_res is None:
            await ctx.send(f"{member.display_name} could not be found in the database. :(")

        elif search_res is not None and len(search_res) > 1:
            await ctx.send(f"""Woops! It looks like there's more than one profile registered to that player. You'll have to be more specific. 
*(Note: this feature is under construction, and is not currently available.)*""")
            # Eventually I'll have to modify this so it works for when you have more than one character...            

        else:
            if args != () and stat_names_listifier(args) == 'Invalid':
                await ctx.send("""Uh oh! I couldn't find that stat. Try one or more of the following, separated by commas:
`hunger, humanity, stains, current willpower, total willpower.`""")

            else:
                if args == ():
                    result = clear_stats(member.id, ctx.author.guild.id, args, True)
                    cleared_msg = f"{member.mention}'s stats have all been reset to 0."
                else:
                    stats = stat_names_listifier(args)
                    print(f"Stats: {stats}/, type: {type(stats)}/, len: {len(stats)}")
                    result = clear_stats(member.id, ctx.author.guild.id, args)
                    if type(stats) == str:
                        cleared_msg = f"{member.mention}'s {column_to_text(stats)} has been reset to 0."
                    elif type(stats) == list and len(stats) == 2:
                        column_list = [column_to_text(thing) for thing in stats]
                        cleared_msg = f"{member.mention}'s {column_list[0]} and {column_list[1]} have been reset to 0."
                    elif type(stats) == list and len(stats) > 2:
                        beginning_results = ', '.join(column_to_text(stats)[:-1])
                        last_result = column_to_text(stats)[-1]
                        cleared_msg == f"{member.mention}'s {beginning_results}, and {last_result} have been reset to 0."
                print(result)
                if result == 'Cleared':
                    await ctx.send(cleared_msg)
                else:
                    await ctx.send("Oops, something went wrong.")


    @clear.command(name='all', aliases=['everyone'])
    async def clear_all(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")
        # clears the stat for all players in guild


    @clear.command(name='table', aliases=['clean_slate'])
    async def clear_table(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")
        # deletes all rows in that table. There will be a default for dynamic_stats, but you can write a table name to make the command more useful in future

    # ----------------------------------------------------------

    ### REMOVE COMMAND GROUP ###

    @commands.group(aliases = ['rem', 'del'], invoke_without_command=True)
    async def remove(self, ctx):
        await ctx.send('Available Humanity Commands: \nhumanity set <number>\nhumanity roll <number of dice> <comments>')


    @remove.command(name='self', aliases=['me'])
    async def remove_self(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")        


    @remove.command(name='other', aliases=['one'])
    async def remove_other(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")        


    @remove.command(name='many', aliases=['others'])
    async def remove_many(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")


    ### Delete all characters that you as a player have in that guild
    # @remove.command(name='all_self', aliases=['me_all', 'del_all_characters'])
    # async def remove_all_self(self, ctx):
    #     await ctx.send("This is a generic message, to use as an example.")    


    ### Deletes all characters that you as a player have, period
    # @remove.command(name='player', aliases=['complete', 'del_player'])
    # async def remove_player(self, ctx):
    #     await ctx.send("This is a generic message, to use as an example.")   

    # ----------------------------------------------------------

    # @command()
    # async def check_tbl(self, ctx, table_name):
    #     result = check_table_exists(table_name)
    #     await ctx.send(f"Table exists: {result}")


def setup(client):
    client.add_cog(Stats(client))
