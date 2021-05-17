import sqlite3

'''
List of all functions in this module:
query_user
db_insert
db_select
db_select_all
db_select_characters
db_update
db_update_basic
db_delete
check_table_exists
delete_table - this one is currently commented out
'''

DB_PATH = "./data/db/database.db"
default_table = 'dynamic_statss' # this is the table where I'm testing stuff on, the "real" one is just 'dynamic_stats'

# TODO: Look more into prepared statements and escape strings..? Because SQLite injection attacks are a thing.
# And like, this is just my own private bot, but good habits are easier to get into sooner than later.
# https://realpython.com/prevent-python-sql-injection/


# TODO: make it so there's a option to query by character name? Not just pull up all names to check if the user exists?
def query_user(userID, guildID, table_name=default_table):
    '''Check if the user is in the database, by pulling up a list of all characters registered to that user in that guild.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f'SELECT character_name FROM {table_name} WHERE user_id = {userID} AND guild_id = {guildID}')
    char_result = cur.fetchall()

    cur.close()
    cxn.close()

    if char_result == []:
        return None
    else:
        return [name[0] for name in char_result]


def db_insert(column_names, Qs, values, table_name=default_table):
    """Insert a new entry into the database, and return the values.
    \n`column_names` need to be formated as a string separated by commas. e.g. 'user_name,user_display_name,user_id,guild_id'
    \n`Qs` is the number of question marks corresponding to the number of column names, separated by commas. e.g. '?,?,?,?,?'"""
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    sql = f'''INSERT INTO {table_name}({column_names[0]})
              VALUES({Qs[0]})
              RETURNING {column_names[0]}'''
    val = values

    cur.execute(sql, val)
    result = cur.fetchone()

    cxn.commit()
    cur.close()
    cxn.close()
    return result


def db_select(userID, guildID, column_names, char_name=False, table_name=default_table):
    '''Look up values in the database for one user or one character for one user.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if char_name == False:
        cur.execute(f"SELECT {column_names[0]} FROM {table_name} WHERE user_id={userID} and guild_id={guildID}")
    elif char_name != False:
        cur.execute(f"SELECT {column_names[0]} FROM {table_name} WHERE user_id={userID} and guild_id={guildID} and character_name='{char_name}'")
        # TODO: change the line above this, because it could be vulnerable to SQLite injection attacks because of char_name

    result = cur.fetchone()
    cur.close()
    cxn.close()
    return result


def db_select_all(guildID, column_names, table_name=default_table):
    '''Look up values in the database, and returns results for all users in that guild.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f"SELECT {column_names[0]} FROM {table_name} WHERE guild_id={guildID}")
    results = cur.fetchall()

    cur.close()
    cxn.close()
    return results


def db_select_characters(userID, guildID, table_name=default_table):
    '''List all the characters belonging to the user.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f"SELECT character_name FROM {table_name} WHERE guild_id={guildID} and user_id={userID}")
    results = cur.fetchall()

    cur.close()
    cxn.close()
    return results


def db_update(userID, guildID, values, column_names, column_Qs, char_name=False, table_name=default_table):
    '''Update values in the database by userID and guildID.
    \n`column_names` and `column_Qs` need to be pre-formatted as strings.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if char_name == False:
        sql = f"""UPDATE {table_name}
                    SET {column_Qs}
                    WHERE user_id = {userID} and guild_id = {guildID}
                RETURNING {column_names[0]} as new_val"""

    elif char_name != False:
        sql = f"""UPDATE {table_name}
                    SET {column_Qs}
                    WHERE user_id = {userID} and guild_id = {guildID} and character_name = '{char_name}'
                RETURNING {column_names[0]} as new_val"""
                # TODO: change the line above this, because it could be vulnerable to SQLite injection attacks because of char_name

    val = values
    cur.execute(sql,val)
    result = cur.fetchone()

    cxn.commit()
    cur.close()
    cxn.close()
    return result


def db_update_basic(guildID, column_Qs, return_column_names, values, where_values=False, table_name=default_table):
    '''
    Update values in the database by guildID. Can add additional where clauses.
    `column_Qs` is a combination of a column name with '=?'. e.g. 'email=?' or 'email=?,phone=?' etc.
    `return_column_names` and `column_Qs` need to be pre-formatted as strings.
    `where_columns` is column names for the where clause, `where_Qs` is the same number of ?s as number of columns in where_columns
    if `where_columns` == False, values = information to be put in the cells that are being updated
    if `where_columns` != False, values = [new updated info for cells, info in where_columns]
    (This is a terrible description, I'm so sorry.)
    '''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if where_values == False:
        sql = f"""UPDATE {table_name}
                    SET {column_Qs}
                    WHERE guild_id = {guildID}
                RETURNING {return_column_names} as new_note"""

    elif where_values != False:
        sql = f"""UPDATE {table_name}
                    SET {column_Qs}
                    WHERE guild_id = {guildID} and {where_values}
                RETURNING {return_column_names} as new_note"""

    val = values
    cur.execute(sql,val)
    result = cur.fetchone()
    cxn.commit()
    cur.close()
    cxn.close()
    return result


def db_delete(column_names, Qs, values, guildID=False, table_name=default_table):
    '''Delete one or more rows from the table'''
    # TODO: Maybe put a limit on quantity?
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if guildID == False:
        sql = f"DELETE from {table_name} WHERE {column_names} IN ({Qs}) RETURNING *"

    elif guildID != False:
        sql = f"DELETE from {table_name} WHERE guild_id={guildID} and {column_names} IN ({Qs}) RETURNING *"

    cur.execute(sql,values)
    results = cur.fetchall()

    n = 0
    print()
    for res in results:
        n=n+1
        print(f"Contents of deleted entry {n} of {len(results)}:\n{res}\n")

    cxn.commit()
    cur.close()
    cxn.close()
    return results


def check_table_exists(table_name):
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name = '{table_name}'")
    result = cur.fetchone()

    cur.close()
    cxn.close()
    if result[0] == 1:
        return True
    elif result[0] == 0:
        return False


# def delete_table(table_name):
#     cxn = sqlite3.connect(DB_PATH)
#     cur = cxn.cursor()
#     cur.execute(f"DROP TABLE IF EXISTS '{table_name}'")
#     cxn.commit()
#     cur.close()
#     cxn.close()

# ---------------------------------------------------------
# ---------------------------------------------------------
