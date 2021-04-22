import sqlite3
import pytz
import datetime
from datetime import datetime, timezone
from math import ceil

from . db_general import query_user, db_insert, db_select, db_select_all, db_select_characters, db_update, db_delete, check_table_exists
from . small_functions import player_info, column_to_text, basic_listifier
from . format_column_names import stat_name_ifs, stat_names_listifier

### These are going to be decommissioned as I edit and streamline the functions and commands associated with them
from . register_lookup import register_player, register, register_variable
from . register_lookup import stats_lookup, stats_lookup_list_all, name_lookup
from . register_lookup import check_table_exists
from . update import update_stats, update_character_name, increment, clear_stats


DB_PATH = "./data/db/database.db"
default_table = 'dynamic_statss'

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

def _register(user_name, user_display_name, userID, guildID, rawinput, char_name=False):
    '''Register a character in the database.'''
    column_names = 'user_name,user_display_name,user_id,guild_id'
    values = [f'{user_name}', user_display_name, userID, guildID]

    if rawinput == ((),) or rawinput == ():
        if char_name == False:
            column_names = (column_names,)
            Qs = ('?,?,?,?',)
        elif char_name != False:
            column_names = (column_names + ',character_name',)
            Qs = ('?,?,?,?,?',)
            values = values + [char_name,]
    else:
        listified_input = stat_names_listifier(rawinput, True)
        if char_name == False:
            column_names = (column_names + ',' + ','.join(listified_input[0]),)
            Qs = ('?,?,?,?,' + ','.join(['?' for x in listified_input[0]]),)
            values = values + listified_input[1]
        elif char_name != False:
            column_names = (column_names + ',character_name,' + ','.join(listified_input[0]),)
            Qs = ('?,?,?,?,?,' + ','.join(['?' for x in listified_input[0]]),)
            values = values + [char_name,] + listified_input[1]

    result = db_insert(column_names, Qs, values)
    return result[4:]


### If you have more than one profile, it will return the first one by rowid
def search(userID, guildID, rawinput, char_name=False, all_columns=False, table_name=default_table):
    '''Search for stats.
    \n`search_all` return results for all stats'''
    if all_columns == True or rawinput == () or rawinput == ((),):
        column_names = ('hunger,humanity,stains,current_willpower,total_willpower,superficial_damage,aggravated_damage,health',)
    elif all_columns == False:
        column_names = (','.join(stat_names_listifier(rawinput)),)

    result = db_select(userID, guildID, column_names, char_name, table_name)
    return result


def _list_all(guildID, rawinput, search_all=False, char_name=False):
    '''List the stats for everyone in the guild.
    \n`char_name` includes character names in the results, as well as user display name.'''
    if search_all == True or rawinput == () or rawinput == ((),):
        column_names = 'user_display_name,hunger,humanity,stains,current_willpower,total_willpower,superficial_damage,aggravataed_damage,health'
    elif search_all == False:
        column_names = 'user_display_name,' + ','.join(stat_names_listifier(rawinput))

    if char_name == True:
        column_names = 'character_name,' + column_names

    result = db_select_all(guildID, (column_names,))
    return result


# TODO: Maybe make it so it automatically updates the user's display name, too?
def _update(userID, guildID, rawinput, char_name=False):
    '''Change your stats.
    \n`char_name` determines which character is being modified, not to change the character's name.'''
    listified_input = stat_names_listifier(rawinput, True)
    column_names = (', '.join(listified_input[0]),)
    values = listified_input[1]
    list_column_Qs = ','.join([title + '=?' for title in listified_input[0]])

    result = db_update(userID, guildID, values, column_names, list_column_Qs, char_name)
    return result