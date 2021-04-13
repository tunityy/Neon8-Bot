import sqlite3
import discord
from string import capwords
from discord import Embed, Member

from . register_lookup import stat_names_listifier
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
