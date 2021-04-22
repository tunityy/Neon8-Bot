import random
from random import randint
import quantumrandom


def raw_results(number_of_dice:int, number_of_sides=10):
    '''Roll some dice!'''
    if number_of_dice == 0 or type(number_of_dice) != int:
        return 'Invalid'
        # return 0
    else:
        return ', '.join(str(random.randint(1, number_of_sides)) for r in range(number_of_dice))


def list_results(raw_roll):
    return list(str(raw_roll).split(", "))


def separate_results(roll_list, determinee:int):
    if determinee == 6:
        return [i for i in list(map(int, roll_list)) if i >= determinee]
    elif determinee == 1 or determinee == 10:
        return [i for i in list(map(int, roll_list)) if i == determinee]
    else:
        print("\n### Error in separate_results function: invalid 'determinee' parameter.\n")


def count_res(roll_list, determinee:int): 
    return int(len(separate_results(roll_list, determinee)))


# It is SUPER SLOW. Not joking.
def true_random_roll(num_dice:int, num_sides=10):
    '''Uses quantum number generation to produce a series of truly random numbers, not pseudo-RNG. \n\nBe warned: this function is EXTREMELY slow.'''
    return ', '.join(str(int(quantumrandom.randint(1, (int(num_sides) + 1)))) for r in range(int(num_dice)))


def quantum_d10(number_of_dice:int):
    '''Uses quantum number generation to produce a series of truly random numbers between 1-10. \n\nBased off the quantumrandom module, this is true RNG, not pseudo-RNG.'''
    remove_decimal = [x for x in str(quantumrandom.randint()) if x != '.']

    while len(remove_decimal) < number_of_dice:
        for y in range(round(number_of_dice/10)):
            remove_decimal = remove_decimal + [x for x in str(quantumrandom.randint()) if x != '.']

    list_of_numbers = [y if y != '0' else '10' for y in remove_decimal]
    return ', '.join(list_of_numbers[y] for y in range(number_of_dice))