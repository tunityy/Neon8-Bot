import sqlite3
# import discord
from string import capwords
# from discord import Embed, Member

DB_PATH = "./data/db/database.db"
default_table = 'dynamic_stats'



def player_info(playerNAME, playerDISPLAY, playerID, guildID):
    return list(str(f"{playerNAME}, {playerDISPLAY}, {playerID}, {guildID}").split(', '))


def query_player(playerID, guildID, table_name=default_table):
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f'SELECT character_name FROM {default_table} WHERE player_id = {playerID} AND guild_id = {guildID}')
    char_result = cur.fetchall()

    cur.close()
    cxn.close()

    if char_result == []:
        return None
    else:
        return [name[0] for name in char_result]


def column_to_text(column_name):
    if column_name == 'current_hunger':
        return 'Hunger'
    else:
        return capwords(column_name.replace('_', ' '))


def basic_listifier(item):
    """Takes strings, tuples, and lists of letters and/or numbers separated by spaces, with and without commas, and returns them in a neat and tidy list (without commas attached at the end."""
    if type(item) == tuple or type(item) == list:
        final = [x.replace(',','') for x in item]
        return final
    elif type(item) == str:
        final = [x.replace(',','') for x in item.split(' ')]
        return final