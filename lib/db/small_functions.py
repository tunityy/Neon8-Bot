import sqlite3
from string import capwords

DB_PATH = "./data/db/database.db"
default_table = 'dynamic_statss'


def player_info(playerNAME, playerDISPLAY, playerID, guildID):
    return list(str(f"{playerNAME}, {playerDISPLAY}, {playerID}, {guildID}").split(', '))


def column_to_text(column_name):
    if type(column_name) == str:
        if column_name == 'current_hunger':
            return 'Hunger'
        else:
            return capwords(column_name.replace('_', ' '))
    else:
        results = [capwords(y.replace('_', ' ')) for y in column_name]
        return results


def basic_listifier(item):
    """Takes strings, tuples, and lists of letters and/or numbers separated by spaces, with and without commas, and returns them in a neat and tidy list (without commas attached at the end."""
    if type(item) == tuple or type(item) == list:
        final = [x.replace(',','') for x in item]
        return final
    elif type(item) == str:
        final = [x.replace(',','') for x in item.split(' ')]
        return final