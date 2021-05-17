from lib.db.db import db_select
from lib.db.db import query_user, db_select, db_insert, _register


def dice_checks(dice_tot, dice_hunger, userID, guildID, user_name=False, user_display_name=False):
    """Under construction"""
    chk = dice_hunger.lower()
    valid = False

    if int(dice_tot) <= 0:
        msg = "**Error**: You can't roll 0 dice!"
        return valid, msg

    else:
        if chk == 'y' or chk == 'yes':
            hunger_stat = db_select(userID, guildID, ('hunger',))
            if hunger_stat is None:
                if int(dice_tot) == 1:
                    dice_hunger = 1
                else:
                    dice_hunger = 2
                res = _register(user_name, user_display_name, userID, guildID, ('hunger', str(dice_hunger)))

                if res == 'Invalid':
                    msg = 'Something went wrong.'
                else:
                    msg = f"**Error**: Could not find player in the database. Registered {user_display_name} as a new player, and set hunger dice to {dice_hunger}."
                    return 'New player', msg, dice_hunger
            elif hunger_stat is not None:
                dice_hunger = hunger_stat[0]

                if dice_hunger == None:
                    dice_hunger = 0

                if dice_hunger > int(dice_tot):
                    dice_hunger = int(dice_tot)
                    msg = f"**Error**: Hunger stat is higher than total dice. The number of hunger dice used for this roll has been adjusted to match total dice."
                    # I don't think I want this to be "Error", but I don't know what else to call it. Warning? FYI? Notice? Heads up??
                    return True, msg, dice_hunger
                else:
                    return True, dice_hunger

        elif chk != 'y' and chk != 'yes':
            try:
                int(dice_hunger)
            except:
                msg = 'Error: variable for hunger dice is invalid. Please use a number, or "y" to use your hunger stat from the database.'

            if int(dice_hunger) > int(dice_tot):
                msg = "**Error**: You can't have more hunger dice than total dice!"
            else:
                valid = True
                msg = int(dice_hunger)
            return valid, msg