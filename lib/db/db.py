import sqlite3
import pytz
import datetime
from datetime import datetime, timezone
from math import ceil

from . db_general import query_user, db_insert, db_select, db_select_all, db_select_characters, db_update, db_update_basic, db_delete, check_table_exists
from . small_functions import column_to_text, basic_listifier, timestamp_mountain, extra_spacing
from . format_column_names import stat_name_ifs, stat_names_listifier

### These are going to be decommissioned as I edit and streamline the functions and commands associated with them
from . register_lookup import stats_lookup, stats_lookup_list_all, name_lookup
from . update import update_stats, update_character_name, increment, clear_stats


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

### -----------------------------------------------


# def query_user(userID, guildID, table_name=default_table):
#     '''Check if the user is in the database, but pulling up a list of all characters registered to that user in that guild.'''
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     cur.execute(f'SELECT character_name FROM {table_name} WHERE user_id = {userID} AND guild_id = {guildID}')
#     char_result = cur.fetchall()

#     cur.close()
#     cxn.close()

#     if char_result == []:
#         return None
#     else:
#         return [name[0] for name in char_result]


# def db_select(userID, guildID, column_names, char_name=False, table_name=default_table):
#     '''Look up values in the database for one user or one character for one user.'''
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     if char_name == False:
#         cur.execute(f"SELECT {column_names[0]} FROM {table_name} WHERE user_id={userID} and guild_id={guildID}")
#     elif char_name != False:
#         cur.execute(f"SELECT {column_names[0]} FROM {table_name} WHERE user_id={userID} and guild_id={guildID} and character_name='{char_name}'")

#     result = cur.fetchone()
#     cur.close()
#     cxn.close()
#     return result


# def db_select_all(guildID, column_names, table_name=default_table):
#     '''Look up values in the database, and returns results for all users in that guild.'''
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     cur.execute(f"SELECT {column_names[0]} FROM {table_name} WHERE guild_id={guildID}")
#     results = cur.fetchall()

#     cur.close()
#     cxn.close()
#     return results


# def db_select_characters(userID, guildID, table_name=default_table):
#     '''List all the characters belonging to the user.'''
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     cur.execute(f"SELECT character_name FROM {table_name} WHERE guild_id={guildID} and user_id={userID}")
#     results = cur.fetchall()

#     cur.close()
#     cxn.close()
#     return results


# def db_update(userID, guildID, values, column_names, column_Qs, char_name=False, table_name=default_table):
#     '''Update values in the database.
#     \n`column_names` and `column_Qs` need to be pre-formatted as strings.'''
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     if char_name == False:
#         sql = f"""UPDATE {table_name}
#                     SET {column_Qs}
#                     WHERE user_id = {userID} and guild_id = {guildID}
#                 RETURNING {column_names[0]} as new_stat_vals"""

#     elif char_name != False:
#         sql = f"""UPDATE {table_name}
#                     SET {column_Qs}
#                     WHERE user_id = {userID} and guild_id = {guildID} and character_name = '{char_name}'
#                 RETURNING {column_names[0]} as new_stat_vals"""
#     val = values
#     cur.execute(sql,val)
#     result = cur.fetchone()

#     cxn.commit()
#     cur.close()
#     cxn.close()
#     return result


# def check_table_exists(table_name):
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name = '{table_name}'")
#     result = cur.fetchone()

#     cur.close()
#     cxn.close()
#     if result[0] == 1:
#         return True
#     elif result[0] == 0:
#         return False


# def db_delete(column_name, column_Qs, values, guildID=False, table_name=default_table):
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     if guildID == False:
#         sql = f"DELETE from {table_name} WHERE {column_name} IN ({column_Qs}) RETURNING *"

#     elif guildID != False:
#         sql = f"DELETE from {table_name} WHERE guild_id={guildID} and {column_name} IN ({column_Qs}) RETURNING *"

#     cur.execute(sql,values)
#     results = cur.fetchall()

#     n = 0
#     print()
#     for res in results:
#         n=n+1
#         print(f"Contents of deleted entry {n} of {len(results)}:\n{res}\n")

#     cxn.commit()
#     cur.close()
#     cxn.close()
#     return results


# def delete_table(table_name):
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()
#     cur.execute(f"DROP TABLE IF EXISTS '{table_name}'")
#     cxn.commit()
#     cur.close()
#     cxn.close()

#### ----------------------------------------------------------

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


### If you have more than one profile, it will return the first one by rowid
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

    
def _reset(userID, guildID):
    '''
    Reset stats to a nice baseline.
    Hunger = 2, Stains and Superficial/Aggravated Damage = 0, Current Willpower = Total Willpower
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


def _increment(userID, guildID, rawinput, char_name=False, table_name=default_table):
    '''Under construction.'''
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


def _delete_user(userID, guildID, confirmation):
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