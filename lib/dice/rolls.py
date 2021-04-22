from . small_functions import raw_results, list_results, separate_results, count_res, true_random_roll, quantum_d10


def v5_roll(dice_tot, dice_hunger, success_req, true_random=False):
# def the_roll_stats(dice_tot, dice_hunger, success_req, true_random=False):
# def the_roll_stats(dice_tot, dice_hunger, success_req, method=1): # use 0 for the method to use quantum RNG
    '''A function for handling dice rolls for v5 Vampire: the Masquerade rules. 
    \n`dice_tot` is the total number of dice
    \n`dice_hunger` is number of hunger dice
    \n`success_req` is the number of successes required
    \n`true_random` enables quantum number generation, for a truly random roll'''
    dice_norm = int(dice_tot) - int(dice_hunger)

    if true_random == False:
        fxn_norm = raw_results(dice_norm)
        fxn_hung = raw_results(dice_hunger)
    elif true_random == True:
        fxn_norm = quantum_d10(dice_norm)
        fxn_hung = quantum_d10(dice_hunger)


    # if method == 1:
    #     fxn_norm = raw_results(dice_norm)
    #     fxn_hung = raw_results(dice_hunger)
    # elif method == 0:
    #     fxn_norm = true_random_roll(dice_norm)
    #     fxn_hung = true_random_roll(dice_hunger)


    if dice_norm == 0:
        norm_roll = "-"
        norm_list = []
    else:
        norm_roll = fxn_norm
        norm_list = list_results(norm_roll)

    norm_10 = count_res(norm_list, 10)
    norm_6 = count_res(norm_list, 6) # this is number of dice that are >= 6. But just writing 6 is easier.

    ### Hunger dice stuff ###
    if int(dice_hunger) == 0:
        hung_roll = "-"
        hung_list = []
    else:
        hung_roll = fxn_hung
        hung_list = list_results(hung_roll)

    hung_10 = count_res(hung_list, 10)
    hung_6 = count_res(hung_list, 6)
    hung_1 = count_res(hung_list, 1)


    ### Calculating successes, criticals, and if the roll passed or failed ###
    total_10s = norm_10 + hung_10
    total_6s = count_res(norm_list, 6) + count_res(hung_list, 6)

    base_value = total_6s - total_10s
    crit_value = (total_10s * 2) - (total_10s % 2)
    success_value_final = crit_value + base_value

    success_get = success_value_final >= int(success_req)
    success_lose = success_value_final < int(success_req)

    passed = success_get == True and success_lose == False
    failed = success_get == False and success_lose == True


    if success_req > 0:
        if failed and hung_1 >= 1:
            res_comment = 'Bestial Failure'
        elif failed and total_6s == 0 and hung_1 == 0:
            res_comment = 'Total Failure'
        elif failed and total_6s >= 1 and hung_1 == 0:
            res_comment = 'Failure'
        elif passed and total_10s <=1:
            res_comment = 'Success'
        elif passed and total_10s >= 2 and hung_10 == 0:
            res_comment = 'Critical Success'
        elif passed and total_10s >=2 and hung_10 >= 1:
            res_comment = 'Messy Critical'
    elif success_req == 0 and total_6s == 0:
        if hung_1 >= 1:
            res_comment = 'Bestial Failure' 
        if hung_1 == 0:
            res_comment = 'Total Failure' 
    else:
        if total_10s <=1:
            res_comment = 'Success\*'
        elif total_10s >= 2 and hung_10 == 0:
            res_comment = 'Possible Critical Success'
        elif total_10s >=2 and hung_10 >= 1:
            res_comment = 'Possible Messy Critical'

    if res_comment == 'Success\*' or res_comment == 'Possible Critical Success' or res_comment == 'Possible Messy Critical':
        res_addn_comment = '\n\* successes needed set at 0, result may be incorrect'
    else:
        res_addn_comment = "\u200b"


    return [
        norm_roll, hung_roll,
        success_value_final,
        res_comment, res_addn_comment
        ]