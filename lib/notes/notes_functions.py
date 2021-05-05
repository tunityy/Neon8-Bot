import sqlite3
import pytz
import datetime
from datetime import datetime, timezone
from math import ceil

from lib.db.small_functions import basic_listifier, timestamp_mountain
from lib.db.db_general import db_insert, db_select, db_select_all, db_update, db_update_basic, db_delete
# from lib.db.db_general import query_user, db_insert, db_select, db_select_all, db_select_characters, db_update, db_delete, check_table_exists

DB_PATH = "./data/db/database.db"

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
        column_names = ('user_name, user_display_name, user_id, guild_id, utc_timestamp, local_timestamp, note_title, note_contents, updateable, edited',)
        Qs = ('?,?,?,?,?,?,?,?,?,?',)

        ts = timestamp_mountain()
        utc_ts = ts[0]
        local_ts = ts[1]

        if updateable == False:
            values = [author_name, author_display_name, authorID, guildID, utc_ts, local_ts, note_title, note_content, 'False', 'False']
        elif updateable == True:
            values = [author_name, author_display_name, authorID, guildID, utc_ts, local_ts, note_title, note_content, 'True', 'False']

        result = db_insert(column_names, Qs, values, 'notes')
        
        if result[6] == note_title:
            return result[6]
        else:
            return result


def db_read_note(notetitle, guildID=False, show_edited=False):
    '''Return the contents of a note in the database, along with the author's display name and time of creation.
    \nIf show_edited=True, will also return if the note has been edited, the editor username and id, and the timestamp of the edit.'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()
    # TODO: Make it return with information about when it was edited and by whom, if applicable

    if show_edited == False:
        if guildID == False:
            sql = f'''SELECT note_contents, user_display_name, local_timestamp, user_id from notes WHERE note_title = ?'''
            val = (notetitle,)
        elif guildID != False:
            sql = f'''SELECT note_contents, user_display_name, local_timestamp, user_id from notes WHERE note_title=? and guild_id=?'''
            notetitle = f'''{notetitle}'''
            val = (notetitle, guildID)
    elif show_edited == True:
        if guildID == False:
            sql = f'''SELECT note_contents, user_display_name, local_timestamp, user_id, edited, edited_by_name, edited_by_display_name, edited_by_id, edit_local_timestamp
            FROM notes
            WHERE note_title = ?'''
            val = (notetitle,)
        elif guildID != False:
            sql = f'''SELECT note_contents, user_display_name, local_timestamp, user_id, edited, edited_by_name, edited_by_display_name, edited_by_id, edit_local_timestamp
            FROM notes
            WHERE note_title=? and guild_id=?'''
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
    # TODO: Limit how many notes can be deleted at once? Maybe make it so only the author and certain people can delete the note?
    if confirmation.lower() != 'yes':
        return "Cancelled, no notes have been deleted."

    elif confirmation.lower() == 'yes':
        values = basic_listifier(note_title)
        column_name = 'note_title'
        column_Qs = ','.join(['?' for title in values])
        result = db_delete(column_name, column_Qs, values, guildID, 'notes')

        if result is None or result == []:
            return 'Error: Note was not deleted because note does not exist'
        else:
            deleted_titles = [res[6] for res in result]
            check_titles = [item if item in deleted_titles else False for item in values]
            undeleted_titles = [item for item in values if item not in deleted_titles]
            
            if False not in check_titles:           
                if len(deleted_titles) == 1:
                    return f'''Note titled "{note_title}" has been deleted.'''
                if len(deleted_titles) == 2:
                    return f'''Notes titled "{deleted_titles[0]}" and "{deleted_titles[1]}" have been deleted'''
                elif len(deleted_titles) > 2:
                    most_res_list = [f'"{x}"' for x in deleted_titles[:-1]]
                    most_results = ', '.join(most_res_list)
                    last_result = f'"{deleted_titles[-1]}"'
                    return f'''Notes titled {most_results}, and {last_result} have been deleted'''
            else:
                return f'''--- __**Error**: Unable to delete all notes__ ---\n
**Successfully Deleted**:  {', '.join(deleted_titles)}
**Could Not Delete**:  {', '.join(undeleted_titles)}'''


def updateable_check(notetitle, guildID=False, userID=False):
    '''Check if the note has the updateable permission enabled'''
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    if guildID == False and userID == False:
        sql = f'''SELECT updateable from notes WHERE note_title=?'''
        val = (notetitle,)
    elif guildID == False and userID != False:
        sql = f'''SELECT updateable from notes WHERE note_title=? and user_id=?'''
        val = (notetitle, userID)
    elif guildID != False and userID == False:
        sql = f'''SELECT updateable from notes WHERE note_title=? and guild_id=?'''
        notetitle = f'''{notetitle}'''
        val = (notetitle, guildID)
    elif guildID != False and userID != False:
        sql = f'''SELECT updateable from notes WHERE note_title=? and guild_id=? and user_id=?'''
        notetitle = f'''{notetitle}'''
        val = (notetitle, guildID, userID)

    cur.execute(sql,val)
    result = cur.fetchone()
    cur.close()
    cxn.close()

    if result is None or result == []:
        if userID == False:
            return 'Note does not exist.'
        elif userID != False:
            return 'Note does not exist, or the user is not the original author of the note.'
    elif result[0] == 'False' or result == 'False':
        return 'Note does not allow edits.'
    elif result[0] == 'True' or result == 'True':
        return True
    else:
        return 'Error: something went wrong with the updateable_check function'


def edit_note_check(notetitle, guildID, userID=False, admin=False, embed_format=True):
    '''Under construction'''
    if admin == False:
        ucheck = updateable_check(notetitle, guildID, userID)
    elif admin != False:
        ucheck = updateable_check(notetitle, guildID)

    ucheck_user = 'Note does not exist, or the user is not the original author of the note.'
    if ucheck == 'Note does not exist.' or ucheck == 'Note does not allow edits.' or ucheck == ucheck_user:
            return 'Problem', ucheck
    elif ucheck == 'Error: something went wrong with the updateable_check function':
        return 'Problem', 'Oops, something went wrong.'

    elif ucheck == True:
        result = db_read_note(notetitle, guildID, True)
        print(result)

        author_id = result[3]
        copy_contents_msg = "Copy the note contents below, edit, and send back."
        cancel_msg = "--- **TYPE 'CANCEL' OR 'NO' TO CANCEL** ---"

        if embed_format == True:
            embed_title = f'''Editing "{notetitle}" by {result[1]}'''

            if result[4] == 'False':
                embed_description = f"""*Created on {result[2][:-10]} at {result[2][11:16]}*\n\n**{copy_contents_msg}**\n```{result[0]}```"""

            elif result[4] == 'True':
                if result[3] == result[7]:
                    embed_description = f"""*Created on {result[2][:-10]} at {result[2][11:16]}*
--- *Last edited on {result[8][:10]}* ---\n\n**{copy_contents_msg}**\n```{result[0]}```"""

                elif result[3] != result[7]:
                    embed_description = f"""*Created by {result[1]} on {result[2][:-10]}*
--- *Last edited by {result[6]} ({result[5][:-5]}) on {result[8][:10]}* ---\n\n**{copy_contents_msg}**\n```{result[0]}```"""

            fields = [("\u200b", f"{cancel_msg}\n\u200b", False)]
            return embed_title, embed_description, author_id, fields

        elif embed_format == False:
            if result[4] == 'False':
                message = f'''__**Editing "{notetitle}" by {result[1]}**__  -  *Created on {result[2][:-10]} at {result[2][11:16]}*
\n{copy_contents_msg}\n```{result[0]}```\n{cancel_msg}'''

            elif result[4] == 'True':
                if result[3] == result[7]:
                    message = f'''__**Editing "{notetitle}" by {result[1]}**__  -  *Created on {result[2][:-10]} at {result[2][11:16]}*
--- Last edited on {result[8][:10]} ---\n\n{copy_contents_msg}\n```{result[0]}```\n{cancel_msg}'''

                elif result[3] != result[7]:
                    message = f'''__**Editing "{notetitle}" by {result[1]}**__  -  *Created by {result[1]} on {result[2][:-10]}*
--- Last edited by {result[6]} ({result[5][:-5]}) on {result[8][:10]} ---\n\n{copy_contents_msg}\n```{result[0]}```\n{cancel_msg}'''
            return message


def fupdate_note(guildID, userID, userNAME, user_display_name, notetitle, new_note_contents, admin=False):
    '''
    Under construction
    `admin` allows someone who is not the original author to edit the note contents. Eventually I'm going to add some kind of check to that.
    '''
    if admin == False:
        ucheck = updateable_check(notetitle, guildID, userID)
    elif admin != False:
        ucheck = updateable_check(notetitle, guildID)

    ucheck_user = 'Note does not exist, or the user is not the original author of the note.'
    if ucheck == 'Note does not exist.' or ucheck == 'Note does not allow edits.' or ucheck == ucheck_user:
        return ucheck
    else:
        return_columns = 'user_display_name, user_id, note_title, edited_by_display_name, edited_by_id, edit_local_timestamp'
        column_Qs = 'note_contents=?,edited=?,edited_by_name=?,edited_by_display_name=?,edited_by_id=?,edit_local_timestamp=?,edit_utc_timestamp=?'
        userNAME = f"{userNAME}"
        ts = timestamp_mountain()
        edit_utc_ts = ts[0]
        edit_local_ts = ts[1]
        column_Qs_vals = [new_note_contents, 'True', userNAME, user_display_name, userID, edit_local_ts, edit_utc_ts]

        if admin == False:
            where_values = f"""guild_id={guildID} and note_title='{notetitle}' and user_id={userID}"""
        elif admin != False:
            where_values = f"""guild_id={guildID} and note_title='{notetitle}'"""

        results = db_update_basic(guildID, column_Qs, return_columns, column_Qs_vals, where_values, 'notes')

        if results == None or results == []:
            return 'Something went wrong'
        elif results[1] == results[4]:
            return f'''Updated "{results[2]}" by {results[3]} on {results[5][:-10]} at {results[5][11:16]}.'''
        else:
            return f'''"{results[2]}" by {results[0]} has been updated by {results[3]} on {results[5][:-10]} at {results[5][11:16]}'''
