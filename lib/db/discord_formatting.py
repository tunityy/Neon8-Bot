from . db import _register, _update, _list_all, search, query_user#, db_select_characters
from . format_column_names import stat_name_ifs, stat_names_listifier, column_to_text

### DON'T FORGET, I NEED TO MAKE THESE FUNCTIONS WORK WITH ROLLING DICE!



def fregister_prompt(raw_numbers):
    numbers_list = basic_listifier(raw_numbers)
    char_info = [item+',' for item in numbers_list[:-1]] + [numbers_list[-1]]
    column_names = ['hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']
    rawinput = [None]*10
    rawinput[::2] = column_names
    rawinput[1::2] = char_info
    return rawinput


def fregister_results(results):
    columns = [column_to_text(x) for x in results[0]]
    zipper = zip(columns, results[1])
    lst = [f'{item[0]} set to {item[1]}'for item in zipper]
    stats = '\n'.join(lst)
    return stats


# def registration(user_name, user_display_name, userID, guildID, rawinput=None, char_name=False, dice=False):
#     '''Register a player and/or character!'''
#     my_result = query_user(userID, guildID)
#     if my_result is not None:
#         msg = "Player is already registered in database."

#     elif my_result is None:
#         print(rawinput)
#         if rawinput is None:
#             rawinput = ()
#         print(rawinput)
#         user_name = f"{user_name}"
#         result = _register(user_name, user_display_name, userID, guildID, rawinput)
#         print(result)
#         if result is None or result is []:
#             msg = "Error: something went wrong."
#         else:
#             print(result[1])
#             return result[1]
#         # await ctx.send(f"""Registered basic player information for **{ctx.author.display_name}** in database.
# # \nNo character stats have been added yet. Please use `.update` or `.set` to enter your stats.""")
#         # print("\n ----- le fin -----")



    # query_result = query_player(playerID, guildID)
    # if query_result is not None:
    #     msg = "Player is already registered in database."

    # elif query_result is None:

    #     raw_result = _register(player_name, player_display_name, playerID, guildID, rawinput, char_name)
    #     print(raw_result)
    #     print(type(raw_result))
        
    #     # Maybe also need a version (different fxn?) of this that does basic player registration for a roll or whatever if the player is not in the database

    #     # Maybe dice arg makes the output different based on whether it's for a dice roll or just a normal command
    #     # So I need to take all this stuff and format it nicely for output in discord



def stat_search(playerID, guildID, rawinput, char_name=False, all_columns=False):
    query_result = query_player(playerID, guildID)
    if query_result is None:
        pass
        # Return something like "Error: player is not registered in the database. Try `newplayer` command to register yourself."
    elif query_result is not None:
        pass

        raw_result = search(playerID, guildID, rawinput, char_name, all_columns)
        print(raw_result)
        print(type(raw_result))

        # have to make this work for nice discord output.
        # if I can make it so ctx.author.whatever and member.mention.whatever both work, that would be grand


def stats_list_all_players(guildID, rawinput, search_all=False, char_name=False):
    if query_result is None:
        pass
        # Return something like "Error: player is not registered in the database. Try `newplayer` command to register yourself."
    elif query_result is not None:
        pass
        raw_result = _list_all(guildID, rawinput, search_all, char_name)
        print(raw_result)
        print(type(raw_result))


def _update_stats():
    if query_result is None:
        pass
        # Register the player, as well as setting the stat/s"
    elif query_result is not None:
        pass


def _clear_stats():
    # makes that stat/s or all stats = 0
    if query_result is None:
        pass
        # Probably just basic register the player
    elif query_result is not None:
        pass


def _reset():
    if query_result is None:
        pass
        # Probably just basic register the player, and maybe set hunger at 2
    elif query_result is not None:
        pass
    # Not sure if I need both? Reset I think should reset stains to 0, hunger to 2, current will = total will, superficial and agg dmg = 0

