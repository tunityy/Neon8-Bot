from . register_lookup import register_player, register, register_variable
from . register_lookup import stats_lookup, stats_lookup_list_all, name_lookup
from . register_lookup import stat_name_ifs, stat_names_listifier
from . register_lookup import check_table_exists

from . general import player_info, query_player, column_to_text, basic_listifier

from . update import update_stats, update_character_name, increment, clear_stats


DB_PATH = "./data/db/database.db"
default_table = 'dynamic_statss'

### -----------------------------------------------

# TODO: make this actually work, move it to register_lookup
def list_chars_by_player(playerID):
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()

    # DB_PATH = "./data/db/database.db"
    cxn = sqlite3.connect(DB_PATH)
    cur = cxn.cursor()
    
    cur.execute("""SELECT character_name FROM dynamic_stats WHERE player_id = ?""", playerID)
    
    myresult = cur.fetchall()
    character_list = []
    
    for x in myresult:
        character_list.append(x[0])
        
    return character_list
    
    cxn.commit()
    cxn.close()