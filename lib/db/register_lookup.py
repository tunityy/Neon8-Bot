import sqlite3
import discord
from string import capwords
from discord import Embed, Member

DB_PATH = "./data/db/database.db"
default_table = 'dynamic_stats'


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

        for item in values_list:
            if item.isdigit() == False:
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


def column_to_text(column_name):
    if column_name == 'current_hunger':
        return 'Hunger'
    else:
        return capwords(column_name.replace('_', ' '))




def stats_lookup(playerID, guildID, stats, search_all=False, char_name=False, table_name=default_table):
    """
`search_all` determines whether the function can look up any number of stats (True), or one fixed number i.e. all of them (False)
\nReplace `char_name` with the actual name of the character instead of True."""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if search_all == True:
        column_names = 'current_hunger, humanity, stains, current_willpower, total_willpower'
        listified_titles = ['current_hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']
        pass
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
    cur.close()
    cxn.close()
    print("Command executed, connection closed.")
    return (listified_titles, results)