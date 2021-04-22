import sqlite3
import pytz
import datetime
from datetime import datetime, timezone
from math import ceil

from lib.db.small_functions import basic_listifier
from lib.db.db_general import db_insert, db_select, db_select_all, db_update, db_delete
# from lib.db.db_general import query_user, db_insert, db_select, db_select_all, db_select_characters, db_update, db_delete, check_table_exists

DB_PATH = "./data/db/database.db"
# default_table = 'dynamic_statss'

'''
List of all functions in this module:
fwrite_note
db_read_note
flist_notes
fdel_note

Under construction:
updateable_check
fupdate_note
'''


def fwrite_note(authorNAME, author_display_name, authorID, guildID, note_title, note_content, updateable=False):
    '''Insert information into the database, including a timestamp in the format YYYY-MM-DD HH:MM.
    Currently does not allow notes with the same title in one guild.'''
    # note_title = args.split('\n', 1)[0]
    # note_content = args.split('\n', 1)[1]

    check_repeat_title = db_select_all(guildID, ('note_title',), 'notes')
    if (note_title,) in check_repeat_title:
        return 'Repeat title'

    elif note_title not in check_repeat_title:
        author_name = f"{authorNAME}"
        column_names = ('user_name, user_display_name, user_id, guild_id, utc_timestamp, local_timestamp, note_title, note_contents, updateable',)
        Qs = ('?,?,?,?,?,?,?,?,?',)

        aware_utc = datetime.now(timezone.utc)
        utc_ts = aware_utc.strftime("%Y-%m-%d %H:%M UTC")
        mountain = pytz.timezone('Canada/Mountain')
        local = mountain.localize(datetime.now())
        local_ts = local.strftime("%Y-%m-%d %H:%M %Z")

        if updateable == False:
            values = [author_name, author_display_name, authorID, guildID, utc_ts, local_ts, note_title, note_content, 'False']
        elif updateable == True:
            values = [author_name, author_display_name, authorID, guildID, utc_ts, local_ts, note_title, note_content, 'True']

        result = db_insert(column_names, Qs, values, 'notes')
        
        if result[6] == note_title:
            return result[6]
        else:
            return result


def db_read_note(notetitle, guildID=False):
    '''Return the contents of a note in the database, along with the author's display name and time of creation.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if guildID == False:
        sql = f'''SELECT note_contents, user_display_name, local_timestamp, user_id from notes WHERE note_title = ?'''
        val = (notetitle,)
    elif guildID != False:
        sql = f'''SELECT note_contents, user_display_name, local_timestamp, user_id from notes WHERE note_title=? and guild_id=?'''
        notetitle = f'''{notetitle}'''
        val = (notetitle, guildID)

    cur.execute(sql,val)
    result = cur.fetchone()
    cur.close()
    cxn.close()
    return result


def flist_notes(guildID, embed=False, field_threshold_1=16, field_threshold_2=32):
    '''
    Return a list of all titles in the notes table.
    `embed` denotes whether the output is put into the format for embed fields for discord, or just a plain string with each title on a new line.
    `field_threshold_1` defines how many titles will appear in the first field before the list gets split in two.
    `field_threshold_2` defines hwo many titles total will be divided in two fields, before the list gets split into three.
    '''
    results = db_select_all(guildID, ('note_title',), 'notes')

    if results  == []:
        return None
    else:
        if embed == False:
            result_list = [item[0] for item in results]
            string_result = '\n'.join(result_list)
            return string_result

        elif embed == True:
                result_list = [item[0] for item in results]
                if len(result_list) <= field_threshold_1:
                    fields = [("\u200b", '\n'.join(result_list), True)]
                    return fields
                else:
                    if field_threshold_1 < len(result_list) <= field_threshold_2:
                        div = 2
                    elif len(result_list) > field_threshold_2:
                        div = 3

                    divide_by = ceil(len(result_list)/div)
                    chunks = [result_list[x:x+divide_by] for x in range(0, len(result_list), divide_by)]
                    fields = [("\u200b", '\n'.join(item), True) for item in chunks]
                    return fields


def fdel_note(note_title, confirmation, guildID):
    '''Delete one or more notes. Requires a confirmation ('yes') so users are less likely to delete a note by accident.'''
    # TODO: Limit how many notes can be deleted at once?
    if confirmation.lower() != 'yes':
        return 'Cancelled'

    elif confirmation.lower() == 'yes':
        values = basic_listifier(note_title)
        column_name = 'note_title'
        column_Qs = ','.join(['?' for title in values])
        result = db_delete(column_name, column_Qs, values, guildID, 'notes')

        if result is None or result == []:
            return None
        else:
            deleted_titles = [res[5] for res in result]
            check_titles = [item if item in deleted_titles else False for item in values]
            undeleted_titles = [item for item in values if item not in deleted_titles]
            
            if False not in check_titles:
                return note_title, deleted_titles
            else:
                return note_title, deleted_titles, undeleted_titles
                return 'Something went wrong'


def updateable_check(notetitle, guildID=False):
    '''Check if the note has the updateable permission enabled'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if guildID == False:
        sql = f'''SELECT updateable from notes WHERE note_title = ?'''
        val = (notetitle,)
    elif guildID != False:
        sql = f'''SELECT updateable from notes WHERE note_title=? and guild_id=?'''
        notetitle = f'''{notetitle}'''
        val = (notetitle, guildID)

    cur.execute(sql,val)
    result = cur.fetchone()
    cur.close()
    cxn.close()

    print(f"Updateable_check result (inside updateable_check): {result}")

    if result is None or result == []:
        return 'Note does not exist.'
    elif result[0] == 'False' or result == 'False':
        return 'Note does not allow edits.'
    elif result[0] == 'True' or result == 'True':
        return True
    else:
        return 'Error: something went wrong with the updateable_check function'


def fupdate_note(notetitle, guildID):
    '''Under construction'''
    ucheck = updateable_check(notetitle, guildID)
    if ucheck == 'Note does not exist.' or ucheck == 'Note does not allow edits.':
        return ucheck
    else:
        pass