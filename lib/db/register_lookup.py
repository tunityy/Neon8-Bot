import sqlite3
import discord
from string import capwords
from discord import Embed, Member

DB_PATH = "./data/db/database.db"
default_table = 'dynamic_stats'

from . general import basic_listifier


### Not using, but it works! ###
def register_player(playerINFO, char_name=False, table_name=default_table):
    """Register a player's basic information into a table."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if char_name == False:
        sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id)
                VALUES(?,?,?,?)"""
        val = (playerINFO)
    elif char_name != False:
        sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id,character_name)
                VALUES(?,?,?,?,?)"""
        playerINFO.append(char_name)
        val = (playerINFO)

    cur.execute(sql, val)
    cxn.commit()
    print(f"Registered {playerINFO[0]} as a player in {table_name}.")

    cur.close()
    cxn.close()



def register(playerINFO, char_name=False, reg_full=False, char_stats=False, table_name=default_table):
    """Register a player and/or character into a table."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if reg_full == False:

        if char_name == False:
            sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id)
                    VALUES(?,?,?,?)"""
            val = playerINFO[0:4]
        elif char_name != False:
            sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id,character_name)
                    VALUES(?,?,?,?,?)"""
            playerINFO.append(char_name)
            val = (playerINFO)

    elif reg_full == True:
        if char_name == False:
            sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id,current_hunger,humanity,stains,current_willpower,total_willpower)
                    VALUES(?,?,?,?,?,?,?,?,?)"""
            playerINFO.extend(char_stats)
            val = (playerINFO)
        elif char_name != False:
            sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id,character_name,current_hunger,humanity,stains,current_willpower,total_willpower)
                    VALUES(?,?,?,?,?,?,?,?,?,?)"""
            playerINFO.append(char_name)
            playerINFO.extend(char_stats)
            val = (playerINFO)

    cur.execute(sql, val)
    cxn.commit()
    print(f"Registered {playerINFO[0]} as a player in {table_name}.")

    cur.close()
    cxn.close()



def register_variable(playerINFO, char_stats, char_name=False, table_name=default_table):
    """Register a player and/or character into a table, with a variable number of stats."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    listified_input = stat_names_listifier(char_stats, True)
    listified_titles = listified_input[0]
    stat_vals = listified_input[1]
    if listified_input == 'Invalid':
        cur.close()
        cxn.close()
        return 'Invalid'

    else:
        listified_input = stat_names_listifier(char_stats, True)
        listified_titles = listified_input[0]
        stat_vals = listified_input[1]
        
        if listified_input == 'Invalid':
            cur.close()
            cxn.close()
            return 'Invalid'

        elif isinstance(listified_input[0], str):  # only 1 stat
            column_title_str = listified_titles
            Qs_length = '?'

        elif isinstance(listified_input[0], list) and len(listified_input[1]) > 1: # more than 1 stat
            column_title_str = ', '.join(listified_titles)
            Qs_length = ','.join(['?' for title in listified_input[0]])

        if char_name == False:
            sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id,{column_title_str})
                    VALUES(?,?,?,?,{Qs_length})
                    RETURNING {column_title_str} as new_stats"""
            val = playerINFO + stat_vals

        elif char_name != False:
            sql = f"""INSERT INTO {table_name}(player_name,player_display_name,player_id,guild_id,character_name,{column_title_str})
                    VALUES(?,?,?,?,?,{Qs_length})
                    RETURNING {column_title_str} as new_stats"""

            val = playerINFO + char_name + stat_vals

    cur.execute(sql, val)
    result = cur.fetchone()
    cxn.commit()
    print(f"Registered {playerINFO[0]} as a player in {table_name}.")
    cur.close()
    cxn.close()
    return listified_titles, result


#### ----------------------------------------------------------


def stat_name_ifs(stat):
    st = str(stat).lower()
    column_name = ['current_hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']

    if st in column_name:
        return st
    else:

        hung_synonyms = ['current_hunger', 'current hunger', 'currenthunger', 'hunger', 'hung',
                         'bp', 'blood pool', 'blood dice', 'bd', 'bloop', 'bloop pool'] # I keep typoing bloop and bloop pool, so fuck it, I'm adding it

        hum_synonyms = ['hum']

        stains_synonyms = ['stain', 'stian'] #more typos

        cwp_synonyms = ['current_willpower', 'current willpower', 'willpower', 'wp', 'currentwillpower', 'currentwp',
                        'will', 'current will', 'current wp', 'cwill', 'c will', 'c wp', 'cwp', 'cw']

        twp_synonyms = ['total_willpower', 'total willpower', 'totalwillpower', 'total wp', 'totalwp', 'twp', 't wp',
                        'totalwill', 'total will', 'willpower total', 'wp total', 'will total', 'wptotal', 'willtotal', 'twill', 'tw', 't will']
        
        if st in hung_synonyms:
            return 'current_hunger'
        elif st in hum_synonyms:
            return 'humanity'
        elif st in stains_synonyms:
            return 'stains'
        elif st in cwp_synonyms:
            return 'current_willpower'
        elif st in twp_synonyms:
            return 'total_willpower'
        else:
            return 'Invalid'

#### ----------------------------------------------------------

def stat_names_listifier(stats, words_and_numbs=False):
    """`words_and_numbs` is to differentiate when stats is just numbers, or contains words and numbers."""
    if words_and_numbs == False:
        list_stats = ' '.join(stats).split(', ')

        if int(len(list_stats)) == 1:
            column_name = stat_name_ifs(list_stats[0])
            return column_name
        else:
            list_of_columns = [stat_name_ifs(term) for term in list_stats]
            if 'Invalid' in list_of_columns:
                return 'Invalid'
            else:
                return list_of_columns

    elif words_and_numbs == True:
        items_to_assess = ' '.join(stats).split(', ')

        list_stats = [item.rsplit(' ', 1)[0] for item in items_to_assess]
        values_list = [item.split(' ')[-1] for item in items_to_assess]

        # for item in values_list:
        #     if item.isdigit() == False:
        #         return 'Invalid'

        for item in values_list:
            try:
                int(item)
            except:
                return 'Invalid'

        if int(len(list_stats)) == 1:
            column_name = stat_name_ifs(list_stats[0])
            if column_name == 'Invalid':
                return 'Invalid'
            else:
                return column_name, values_list
        else:
            list_of_columns = [stat_name_ifs(term) for term in list_stats]
            if 'Invalid' in list_of_columns:
                return 'Invalid'
            else:
                return list_of_columns, values_list


#### ----------------------------------------------------------


def stats_lookup(playerID, guildID, stats, search_all=False, char_name=False, table_name=default_table, show_none=False):
    """
`search_all` determines whether the function can look up any number of stats (True), or one fixed number i.e. all of them (False)
\nReplace `char_name` with the actual name of the character instead of True.
\nWhen `show_none` is False then results that are None or '' are replaced with the integer 0. `show_none=True` means results are given as-is."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if search_all == True:
        column_names = 'current_hunger, humanity, stains, current_willpower, total_willpower'
        listified_titles = ['current_hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']
    elif search_all == False:
        listified_titles = stat_names_listifier(stats)
        if listified_titles == 'Invalid':
            cur.close()
            cxn.close()
            return 'Invalid'

        elif isinstance(listified_titles, str): ## Only 1 stat
            column_names = listified_titles
            listified_titles = [listified_titles]
        elif isinstance(listified_titles, list) and len(listified_titles) > 1: ## More than 1 stat
            column_names = ', '.join(listified_titles)

    if char_name == False:
        cur.execute(f"SELECT {column_names} FROM {table_name} WHERE player_id={playerID} and guild_id={guildID}")
    elif char_name != False:
        cur.execute(f"SELECT {column_names} FROM {table_name} WHERE player_id={playerID} and guild_id={guildID} and character_name='{char_name}'")

    result = cur.fetchone()
    cxn.commit()
    cur.close()
    cxn.close()

    if show_none == False:
        if char_name == False:
            if result == ('',) or result == (None,):
                result = (0,)
            elif len(result) == 1 and result != ('',):
                result = result
            else:
                result = tuple([0 if item == '' or item is None else item for item in result])
        else: # i.e. elif char_name !=:
            result = result ## I'll probably have to fix this in future, but that's a problem for future me

    elif show_none == True:
        result = result

    print("Searched the thing.")
    return listified_titles, result



def stats_lookup_list_all(playerID, guildID, stats, search_all=False, table_name=default_table):
    """Returns the specified stat or stats for all players in the guild.
playerID, guildID, stats, search_all=True, table_name=default_table
<search_all> determines whether the function can look up any number of stats (True), or one fixed number i.e. all of them (False)."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if search_all == True:
        column_names = 'current_hunger, humanity, stains, current_willpower, total_willpower'
        listified_titles = ['current_hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']
    else:
        listified_titles = stat_names_listifier(stats)
        if listified_titles == 'Invalid':
            cur.close()
            cxn.close()
            return 'Invalid'

        elif isinstance(listified_titles, str): ## Only 1 stat
            column_names = listified_titles
            listified_titles = [listified_titles]
        elif isinstance(listified_titles, list) and len(listified_titles) > 1: ## More than 1 stat
            column_names = ', '.join(listified_titles)

    cur.execute(f"SELECT player_display_name, {column_names} FROM {table_name} WHERE guild_id={guildID}")

    results = cur.fetchall()
    # results = [tup[:1]+tuple([0 if item == '' or item is None else item for item in tup[1:]]) for tup in results]
    # TODO: fix this

    cur.close()
    cxn.close()
    print("Command executed, connection closed.")
    return (listified_titles, results)


#### ----------------------------------------------------------


def name_lookup(playerID, guildID, search_all=False, table_name=default_table):
    """`search_all` will return a list of all characters for that player."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f"SELECT character_name FROM {table_name} WHERE player_id={playerID} and guild_id={guildID}")

    if search_all == True:
        result = cur.fetchall()
    elif search_all == False:
        result = cur.fetchone()

    cxn.commit()
    cur.close()
    cxn.close()
    print("Name has been found.")
    return result

#### ----------------------------------------------------------


def check_table_exists(table_name):
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name = '{table_name}'")
    result = cur.fetchone()

    if result[0] == 1:
        return True
    elif result[0] == 0:
        return False

    cur.close()
    cxn.close()