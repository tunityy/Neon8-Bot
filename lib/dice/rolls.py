# from . small_functions import raw_results, true_random_roll, quantum_d10
import random
from random import randint
import quantumrandom


def raw_results(number_of_dice:int, number_of_sides=10):
    '''Roll some dice!'''
    if number_of_dice == 0 or type(number_of_dice) != int:
        return 'Invalid'
    else:
        num_sides = int(number_of_sides)
        num_dice = int(number_of_dice)
        return [randint(1, num_sides) for r in range(num_dice)]


# It is SUPER SLOW. Not joking.
def true_random_roll(num_dice:int, num_sides=10):
    '''Uses quantum number generation to produce a series of truly random numbers, not pseudo-RNG. \n\nBe warned: this function is EXTREMELY slow.'''
    num_dice = int(num_dice)
    num_sides = int(num_sides)
    return [int(quantumrandom.randint(1, num_sides + 1)) for r in range(num_dice)]


def quantum_d10(number_of_dice:int):
    '''
    Uses quantum number generation to produce a series of truly random numbers between 1-10.
    Based off the quantumrandom module, this is true RNG, not pseudo-RNG.
    '''
    remove_decimal = [x for x in str(quantumrandom.randint()) if x != '.']

    while len(remove_decimal) < number_of_dice:
        for y in range(round(number_of_dice/10)):
            remove_decimal = remove_decimal + [x for x in str(quantumrandom.randint()) if x != '.']

    list_of_numbers = [int(y) if y != '0' else 10 for y in remove_decimal]
    return [list_of_numbers[y] for y in range(number_of_dice)]


def v5_roll(dice_tot, dice_hunger, success_req, true_random=False):
    '''A function for handling dice rolls for v5 Vampire: the Masquerade rules. 
    \n`dice_tot` is the total number of dice
    \n`dice_hunger` is number of hunger dice
    \n`success_req` is the number of successes required
    \n`true_random` enables quantum number generation, for a truly random roll'''
    dice_norm = int(dice_tot) - int(dice_hunger)

    if dice_norm == 0:
        norm_roll = "-"
        norm_list = []
    else:
        if true_random == False:
            norm_list = raw_results(dice_norm)
        elif true_random == True:
            norm_list = quantum_d10(dice_norm)
        norm_roll = ', '.join(f'{item}' for item in norm_list)            

    norm_10 = len([i for i in norm_list if i == 10])
    norm_6 = len([i for i in norm_list if i >= 6])

    ### Hunger dice stuff ###
    if int(dice_hunger) == 0:
        hung_roll = "-"
        hung_list = []
    else:
        if true_random == False:
            hung_list = raw_results(dice_hunger)
        elif true_random == True:
            hung_list = quantum_d10(dice_hunger)
        hung_roll = ', '.join(f'{item}' for item in hung_list)     

    hung_10 = len([i for i in hung_list if i == 10])
    hung_6 = len([i for i in hung_list if i >= 6])
    hung_1 = len([i for i in hung_list if i == 1])

    ### Calculating successes, criticals, and if the roll passed or failed ###
    total_10s = norm_10 + hung_10
    total_6s = norm_6 + hung_6   

    base_value = total_6s - total_10s
    crit_value = (total_10s * 2) - (total_10s % 2)
    success_value_final = crit_value + base_value

    passed = success_value_final >= int(success_req)
    failed = success_value_final < int(success_req)

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