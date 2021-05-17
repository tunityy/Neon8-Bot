import sqlite3
import pytz
import datetime
from datetime import datetime, timezone
from math import ceil

from . db_general import query_user, db_insert, db_select, db_select_all, db_select_characters, db_update, db_update_basic, db_delete, check_table_exists
from . small_functions import column_to_text, basic_listifier, timestamp_mountain, extra_spacing
from . format_column_names import stat_name_ifs, stat_names_listifier

# ### These are going to be decommissioned as I edit and streamline the functions and commands associated with them
# from . register_lookup import stats_lookup, stats_lookup_list_all, name_lookup
# from . update import update_stats, update_character_name, increment, clear_stats

from lib.dice.rolls import raw_results


'''
List of all functions in this module:
fregister_prompt
fregister_results
fsearch

_register
search
_list_all
_update
_reset
_increment
_delete_user
'''


DB_PATH = "./data/db/database.db"
default_table = 'dynamic_statss'
es = extra_spacing


# TODO: make it so everything that involves updating the table at all will update the person's display name at the same time?
# TODO: almost maybe just make a command to update your display name?


def fregister_prompt(raw_numbers):
    '''Format numbers from a prompt to register player and enter values for the five basic stats.'''
    numbers_list = basic_listifier(raw_numbers)
    char_info = [item+',' for item in numbers_list[:-1]] + [numbers_list[-1]]
    column_names = ['hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']
    rawinput = [None]*10
    rawinput[::2] = column_names
    rawinput[1::2] = char_info
    return rawinput


def fregister_results(results):
    '''Format results from registering a player'''
    results = list(results)
    if type(results[0]) != list:
        results[0] = results[0][0].split(', ')
    columns = [column_to_text(x) for x in results[0]]
    zipper = zip(columns, results[1])
    lst = [f'{item[0]} set to {item[1]}'for item in zipper]
    stats = '\n'.join(lst)
    return stats


def fsearch(results):
    '''Format search results'''
    col = results[0][0].split(', ')
    columns = [column_to_text(x) for x in col]
    numbs = [0 if x == None else x for x in results[1]]
    zipper = zip(columns, numbs)

    lst = [f'{item[0]}: {es(2)} {item[1]}' for item in list(zipper)]
    stats = f'{es(3)} \n'.join(lst)
    return stats


def _register(user_name, user_display_name, userID, guildID, rawinput, char_name=False):
    '''
    Register a character in the database.
    `rawinput` is used for inserting stats at the same time, along with the player information
    '''
    column_names = 'user_name,user_display_name,user_id,guild_id'
    values = [f'{user_name}', user_display_name, userID, guildID]

    if rawinput == ((),) or rawinput == ():
        columns = False
        if char_name == False:
            column_names = (column_names,)
            Qs = ('?,?,?,?',)
        elif char_name != False:
            column_names = (column_names + ',character_name',)
            Qs = ('?,?,?,?,?',)
            values = values + [char_name,]
    else:
        listified_input = stat_names_listifier(rawinput, True)
        columns = listified_input[0]
        print("inside _register")
        print(listified_input)
        if listified_input == 'Invalid' or listified_input[0] == 'Invalid' or listified_input[0][0] == 'Invalid':
            return 'Invalid'

        if char_name == False:
            column_names = (column_names + ',' + ','.join(columns),)
            Qs = ('?,?,?,?,' + ','.join(['?' for x in columns]),)
            values = values + listified_input[1]
        elif char_name != False:
            column_names = (column_names + ',character_name,' + ','.join(listified_input[0]),)
            Qs = ('?,?,?,?,?,' + ','.join(['?' for x in listified_input[0]]),)
            values = values + [char_name,] + listified_input[1]

    result = db_insert(column_names, Qs, values)
    if columns is False:
        return result[4:]
    else:
        return columns, result[4:]


# If you have more than one profile, it will return the first one by rowid. So I might want to change that?
def search(userID, guildID, rawinput, char_name=False, all_columns=False, table_name=default_table):
    '''Search for stats.
    \n`search_all` return results for all stats'''

    if all_columns == True or rawinput == () or rawinput == ((),):
        column_names = ('hunger, humanity, stains, current_willpower, total_willpower, superficial_damage, aggravated_damage, health',)
        listified_columns = ('',)
    elif all_columns == False:
        listified_columns = stat_names_listifier(rawinput)
        column_names = (', '.join(listified_columns),)

    if listified_columns == 'Invalid' or listified_columns[0] == 'Invalid':
        return 'Invalid'
    else:
        result = db_select(userID, guildID, column_names, char_name, table_name)
        return column_names, result


def _list_all(guildID, rawinput, search_all=False, char_name=False):
    '''List the stats for everyone in the guild.
    \n`char_name` includes character names in the results, as well as user display name.'''
    if search_all == True or rawinput == () or rawinput == ((),):
        listified_columns = ((),)
        column_names = 'user_display_name, hunger, humanity, stains, current_willpower, total_willpower, superficial_damage, aggravated_damage, health'
    elif search_all == False:
        listified_columns = stat_names_listifier(rawinput)
        column_names = 'user_display_name,' + ', '.join(listified_columns)

    if char_name == True:
        column_names = 'character_name,' + column_names

    if listified_columns == 'Invalid' or listified_columns[0] == 'Invalid':
        return 'Invalid'
    else:
        result = result = db_select_all(guildID, (column_names,))
        return column_names, result


# TODO: Maybe make it so it automatically updates the user's display name, too?
def _update(userID, guildID, rawinput, char_name=False):
    '''Change your stats.
    \n`char_name` determines which character is being modified, not to change the character's name.'''
    listified_input = stat_names_listifier(rawinput, True)

    if listified_input == 'Invalid' or listified_input[0] == 'Invalid':
        return 'Invalid'
    else:
        column_names = (', '.join(listified_input[0]),)
        values = listified_input[1]
        list_column_Qs = ','.join([title + '=?' for title in listified_input[0]])

        # print(f"Inside _update\n{values}\n{column_names}\n{list_column_Qs}\nEnd\n")
        before_result = db_select(userID, guildID, column_names)
        result = db_update(userID, guildID, values, column_names, list_column_Qs, char_name)

        return column_names, result#, before_result

    
# TODO: make it work with character names
# TODO: (maybe) make it integrate with a "guild settings" table in the database for what values to use for the defaults
def _reset(userID, guildID, char_name=False):
    '''
    Reset stats to a nice baseline.
    Hunger = 2, Stains and Superficial/Aggravated Damage = 0, Current Willpower = Total Willpower
    Resetting a character by name to be implemented in future.
    '''
    stats = db_select(userID, guildID, ('hunger,humanity,stains,current_willpower,total_willpower,superficial_damage,aggravated_damage,health',))
    before_stats = [0 if stat is None else stat for stat in list(stats)]
    # before_stats = [0 if stat is None or stat == '' else stat for stat in list(stats)]
    twill = before_stats[4]

    column_names = ('hunger, humanity, stains, current_willpower, total_willpower, superficial_damage, aggravated_damage, health',)
    column_Qs = 'hunger=?,stains=?,current_willpower=?,total_willpower=?,superficial_damage=?,aggravated_damage=?'
    val = [2,0,twill,twill,0,0]
    values = [str(x) for x in val]

    res = db_update(userID, guildID, values, column_names, column_Qs)

    if res == (2, stats[1], 0, twill, twill, 0, 0, stats[7]):
        return column_names, res#,  before_stats
    else:
        return 'Something went wrong'


# TODO: make it work with character names. But make sure that it's safe from SQLite injection!
def _increment(userID, guildID, rawinput, char_name=False, table_name=default_table):
    '''Under construction. Character name has not been implemented at all at this time.'''
    listified_input = stat_names_listifier(rawinput)

    if listified_input == 'Invalid' or listified_input[0] == 'Invalid':
        listified_input = stat_names_listifier(rawinput, True)

    if listified_input == 'Invalid' or listified_input[0] == 'Invalid' or listified_input[0][0] == 'Invalid':
        return 'Invalid'

    else:
        if len(listified_input) == 1:
            stat_column = (listified_input[0],)
            column_name = ('user_id,' + listified_input[0],)
            increment = 1
        elif len(listified_input) == 2:
            stat_column = listified_input[0]
            column_name = ['user_id,' + listified_input[0][0]]
            increment = int(listified_input[1][0])

        val = db_select(userID, guildID, column_name)

        if val is None or val[0] is None:
            return None
        else:
            column_Q = stat_column[0] + '=?'
            if val[1] is None:
                value = [increment]
            else:
                value = [val[1]+increment]
            result = db_update(userID, guildID, value, stat_column, column_Q, char_name, table_name)
            return (result[0] - increment), result[0], column_to_text(stat_column)[0]


# TODO: make it work with character names
def _delete_user(userID, guildID, confirmation, char_name=False):
    '''Delete a user from the database. Currently deletes a user entirely; in future I hope to add functionality so you can delete by character name.'''
    if confirmation.lower() != 'yes':
        return "Cancelled, user has not been deleted."
        
    elif confirmation.lower() == 'yes':
        column_names = 'user_id'
        Qs = '?'
        values = [userID]

        result = db_delete(column_names, Qs, values, guildID)[0]

        if userID == result[-2]:
            return f'User {result[0]} successfully deleted'
        else:
            return 'Something went wrong'


# TODO: make it work with character names
def _remorse(userID, guildID, user_display_name, char_name=False):
    '''Under construction'''
    my_result = query_user(userID, guildID)
    if my_result is None:
        return False, """Player is not registered in the database.
Use `.set humanity x, stains y` (replacing x and y with the appropriate values) to register and set your stats, then try again."""

    elif my_result is not None:
        stats = search(userID, guildID, ('humanity,', 'stains'))
        hum = stats[1][0]
        stain = stats[1][1]

        if stain == 0 or stain == None:
            # I don't love the look of this message, so I want to change it at some point
            return False, f"**Auto-success**: *{user_display_name}* has zero stains.\n\nIf this is a mistake, use `.set stain x` to set your stains, then try again."
        else:
            if hum == 0 or hum == None:
                return False, "Player does not have their humanity stat set!\nUse `.set humanity x` to set your humanity, then try again."

            else:
                error_msg = False

                empty_dots = 10 - hum - stain
                if empty_dots > 0:
                    dice = empty_dots

                elif empty_dots <= 0:
                    dice = 1
                    # msg = f"{user_display_name} had more Stains than empty boxes on the Humanity track. Number of dice for the remorse roll is 1."

                rolls = raw_results(dice)
                stringified_rolls = ', '.join(f'{item}' for item in rolls)

                wins = len([i for i in rolls if i >= 6])

                if wins > 0:
                    new_stain = _update(userID, guildID, ('stains', '0'))
                    remorse_msg = f"{user_display_name} has suffered enough guilt, shame, or regret to retain their current Humanity. All Stains have been removed."

                else:
                    new_hum_result = _increment(userID, guildID, ('humanity', '-1'))
                    if new_hum_result == 'Invalid':
                        error_msg = "Something went wrong. Unable to change humanity stat."
                    elif new_hum_result is None:
                        error_msg = "Something went REALLY wrong. Unable to change humanity stat."

                    else:
                        old_hum = int(new_hum_result[0])
                        new_hum = int(new_hum_result[1])

                        if new_hum == old_hum -1:
                            new_stain = _update(userID, guildID, ('stains', '0'))
                            remorse_msg = f"The Beast has won. {user_display_name} justifies their actions to themselves, and loses a part of their remaining Humanity as a result. All Stains have been removed."
                        else:
                            error_msg = "Something went wrong with changing the humanity stat. Please get the bot owner to look into it."

                if error_msg is False:
                    msg = remorse_msg
                else:
                    msg = f"{remorse_msg}\n\* {error_msg}"

                # I just realized I probably want to include New Humanity in the results if the person fails their remorse check
                final_msg = f"Remorse Roll for {user_display_name}\nCurrent Humanity: {hum}\nStains: {stain}\nDice Results: {stringified_rolls}\nResults: {msg}"
                return True, final_msg


# TODO: make it work with character names
# def degen_chk(userID, guildID, char_name=False):
def degeneration_check(userID, guildID, char_name=False):
    '''
    Under construction
    Assumes that query_user has already been used to establish if a character/user is in the database
    '''
    print("\n----- Inside degeneration_check")
    stats = search(userID, guildID, ('humanity,', 'stains'))
    hum = stats[1][0]
    stain = stats[1][1]

    if stain == 0 or stain == None:
        return False, "Player has no stains. Degeneration does not apply"
    else:
        if hum == 0 or hum == None:
            return False, """Player does not have their humanity stat set!\nUse `.set humanity x` set your humanity, then try again."""

        empty_dots = 10 - hum

        if empty_dots >= stain:
            print("Passed degeneration check\nEnd degeneration check ------\n")
            return False
        elif empty_dots < stain:
            # maybe do more paraphrasing and less direct quoting? Or maybe use quotation marks to indicate that I am quoting?
            msg = """Degeneration, page 239.

The character becomes Impaired, overcome with regret. This causes the following:
- They take a two-dice penalty to all pools.
- They take 1 point of Aggravated Willpower damage for each Stain that could not fit in the empty boxes of their Humanity track.
- The are incapable of further intentional Tenet violations, and if forced to commit one, they must test for terror frenzy (Difficulty 4).

The character remains Impaired until the end of the session, when Remorse is tested.
The character can also choose to snap out of it by voluntarily losing a point of Humanity, wiping away the Stains as they rationalize their actions and accept what they’ve become."""

            print("Failed degeneration check\nEnd degeneration check ------\n")
            return True, msg
