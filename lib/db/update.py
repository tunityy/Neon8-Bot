import sqlite3
import discord
from string import capwords
from discord import Embed, Member

from . register_lookup import stat_name_ifs, stat_names_listifier, stats_lookup, stats_lookup_list_all
from . general import basic_listifier

DB_PATH = "./data/db/database.db"
default_table = 'dynamic_stats'



def update_stats(playerID, guildID, raw_input, update_all=False, char_name=False, table_name=default_table):
    """Update your stats! :)"""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if update_all == True:
        column_title_str = 'current_hunger, humanity, stains, current_willpower, total_willpower'
        columns_Qs = 'current_hunger=?, humanity=?, stains=?, current_willpower=?, total_willpower=?'
        stat_vals = basic_listifier(raw_input)
        listified_titles = ['current_hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']

    elif update_all == False:
        listified_input = stat_names_listifier(raw_input, True)
        listified_titles = listified_input[0]
        stat_vals = listified_input[1]
        if listified_input == 'Invalid':
            cur.close()
            cxn.close()
            return 'Invalid'

        elif isinstance(listified_input[0], str):  # only 1 stat
            column_title_str = listified_titles
            columns_Qs = column_title_str + '=?'

        elif isinstance(listified_input[0], list) and len(listified_input[1]) > 1: # more than 1 stat
            column_title_str = ', '.join(listified_titles)
            list_column_Qs = [title + '=?' for title in listified_titles]
            columns_Qs = ', '.join(list_column_Qs)

    if char_name == False:
        sql = f"""UPDATE {default_table}
                    SET {columns_Qs}
                    WHERE player_id = {playerID} and guild_id = {guildID}
                RETURNING {column_title_str} as new_stat_vals"""

    elif char_name != False:
        sql = f"""UPDATE {default_table}
                    SET {columns_Qs}
                    WHERE player_id = {playerID} and guild_id = {guildID} and character_name = '{char_name}'
                RETURNING {column_title_str} as new_stat_vals"""

    cur.execute(sql,stat_vals)
    result = cur.fetchone()
    cxn.commit()
    cur.close()
    cxn.close()

    print("Done, son.")
    return listified_titles, result


#### ----------------------------------------------------------


def update_character_name(playerID, guildID, name, select_character=False, table_name=default_table):
# def update_name(playerID, guildID, raw_input, update_all=False, char_name=False, table_name=default_table):
    """Update your character's name! :)"""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if select_character == False:
        sql = f"""UPDATE {table_name}
                    SET character_name=?
                    WHERE player_id = {playerID} and guild_id = {guildID}
                RETURNING character_name as new_name"""

    elif select_character == True:
        sql = f"""UPDATE {table_name}
                    SET character_name=?
                    WHERE player_id = {playerID} and guild_id = {guildID} and character_name = '{select_character}'
                RETURNING character_name as new_name"""
    val = name

    cur.execute(sql, val)
    result = cur.fetchone()
    cxn.commit()
    cur.close()
    cxn.close()

    print("Name changed.")
    return result


#### ----------------------------------------------------------


def increment(playerID, guildID, stat_name, increase_by=1, char_name=False, table_name=default_table):
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()
    stat = basic_listifier(stat_name)
    stat_search = stats_lookup(playerID, guildID, basic_listifier(stat_name), show_none=True)
    stat_column = stat_search[0][0]
    if stat_search == 'Invalid' or stat_column == 'Invalid':
        cur.close()
        cxn.close()
        return 'Invalid'

    if stat_search[1][0] is None:
        if char_name == False:
            sql = f"""UPDATE {table_name}
                        SET '{stat_column}'=?
                        WHERE player_id = {playerID} and guild_id = {guildID}
                    RETURNING {stat_column} as new_stat_val"""
        elif char_name != False:
            sql = f"""UPDATE {table_name}
                        SET '{stat_column}'=?
                        WHERE player_id = {playerID} and guild_id = {guildID} and character_name = '{char_name}'
                    RETURNING {stat_column} as new_stat_val"""
        val = str(increase_by)
        cur.execute(sql, val)

    else:
        if char_name == False:
            cur.execute(f"""UPDATE {table_name}
                        SET {stat_column} = {stat_column} + {str(increase_by)}
                        WHERE player_id={playerID} and guild_id={guildID}
                    RETURNING {stat_column} as new_stat_val""")
        elif char_name != False:
            cur.execute(f"""UPDATE {table_name}
                        SET '{stat_column}' = '{stat_column}' + {str(increase_by)}
                        WHERE player_id=? and guild_id=? and character_name=?
                    RETURNING {stat_column} as new_stat_val""")
    result = cur.fetchone()
    cxn.commit()

    cur.close()
    cxn.close()

    return result

#### ----------------------------------------------------------

def clear_stats(playerID, guildID, stats, clear_row=False, char_name=False, table_name=default_table):
    """Clear your stats"""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if clear_row == True:
        column_title_str = 'current_hunger, humanity, stains, current_willpower, total_willpower'
        columns_Qs = 'current_hunger=?, humanity=?, stains=?, current_willpower=?, total_willpower=?'
        stat_vals = ('0', '0', '0', '0', '0')
        listified_titles = ['current_hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower']

    elif clear_row == False:
        listified_titles = stat_names_listifier(stats)
        if listified_titles == 'Invalid':
            cur.close()
            cxn.close()
            return 'Invalid'

        elif isinstance(listified_titles, str):  # only 1 stat
            column_title_str = listified_titles
            columns_Qs = column_title_str + '=?'
            stat_vals = [0,]

        elif isinstance(listified_titles, list): # more than 1 stat
            column_title_str = ', '.join(listified_titles)
            list_column_Qs = [title + '=?' for title in listified_titles]
            columns_Qs = ', '.join(list_column_Qs)
            stat_vals = ['0' for item in listified_titles]

    if char_name == False:
        sql = f"""UPDATE {table_name}
                    SET {columns_Qs}
                    WHERE player_id = {playerID} and guild_id = {guildID}
                RETURNING {column_title_str} as new_stat_vals"""

    elif char_name != False:
        sql = f"""UPDATE {table_name}
                    SET {columns_Qs}
                    WHERE player_id = {playerID} and guild_id = {guildID} and character_name = '{char_name}'
                RETURNING {column_title_str} as new_stat_vals"""

    cur.execute(sql,stat_vals)
    result = cur.fetchone()
    cxn.commit()
    cur.close()
    cxn.close()


    print("Done, son.")
    if len(result) == 1 and result == (0,):
        return 'Cleared'
    elif len(result) > 1:
        for item in result:
            if item == 0:
                pass
            else:
                return 'Something went wrong'
        return 'Cleared'
    else:
        return 'Something went wrong'



#### ----------------------------------------------------------

# def delete_table(table_name):
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()

#     print(table_name)
#     cur.execute(f"DROP TABLE IF EXISTS '{table_name}'")

#     cxn.commit()
#     cur.close()
#     cxn.close()

#     print("Command has been executed. Table has been deleted.")        