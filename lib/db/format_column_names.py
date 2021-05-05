def column_to_text(column_name):
    if type(column_name) == str:
        return capwords(column_name.replace('_', ' '))
    else:
        results = [capwords(y.replace('_', ' ')) for y in column_name]
        return results


def stat_name_ifs(stat):
    st = str(stat).lower()
    column_name = ['hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower', 'superficial_damage', 'aggravated_damage', 'health']

    if st in column_name:
        return st
    else:
        # some of these include common or possible typos and misspellings
        hung_synonyms = ['current_hunger', 'current hunger', 'currenthunger', 'hung', 'hungry'
                         'bp', 'blood pool', 'blood dice', 'bd', 'bloop', 'bloop pool']
        hum_synonyms = ['hum', 'huemanatee', 'hue manatee', 'humane', 'human']
        stains_synonyms = ['stain', 'stian', 'st', 'stians', 'stans']
        cwp_synonyms = ['current_willpower', 'current willpower', 'willpower', 'wp', 'currentwillpower', 'currentwp',
                        'will', 'current will', 'current wp', 'cwill', 'c will', 'c wp', 'cwp', 'cw', 'c w']
        twp_synonyms = ['total willpower', 'totalwillpower', 'total wp', 'totalwp', 'twp', 't wp', 'total', 'tot',
                        'totalwill', 'total will', 'willpower total', 'wp total', 'will total', 'wptotal', 'willtotal', 'twill', 'tw', 't will']
        spr_dmg_synonyms = ['superficial', 'superficial dmg', 'superficialdmg', 'sdmg', 'sdamage', 's damage', 'sdmg', 'super']
        agg_dmg_synonyms = ['agg', 'aggravated', 'aggr', 'agg dmg', 'aggdmg', 'aggr dmg', 'aggrdmg', 'aggravateddmg', 'aggravated dmg',
                            'aggravated damage', 'admg', 'adamage', 'a dmg', 'a damage', 'aggravateddamage',
                            'aggrivated', 'aggrivated damage', 'aggrevated', 'aggrevated damage', 'aggrevated dmg', 'aggrivated dmg']
        health_synonyms = ['hp', 'hitpoints', 'hit points', 'health bar', 'healthbar']

        if st in hung_synonyms:
            return 'hunger'
        elif st in hum_synonyms:
            return 'humanity'
        elif st in stains_synonyms:
            return 'stains'
        elif st in cwp_synonyms:
            return 'current_willpower'
        elif st in twp_synonyms:
            return 'total_willpower'
        elif st in spr_dmg_synonyms:
            return 'superficial_damage'
        elif st in agg_dmg_synonyms:
            return 'aggravated_damage'
        elif st in health_synonyms:
            return 'health'
        else:
            return 'Invalid'

#### ----------------------------------------------------------

### TODO: when it's just a list of one word it actually just comes out as a string. Need to change it to a list
def stat_names_listifier(stats, words_and_numbs=False):
    """`words_and_numbs` is to differentiate when stats is just numbers, or contains words and numbers."""
    if words_and_numbs == False:
        list_stats = ' '.join(stats).split(', ')

        if int(len(list_stats)) == 1:
            column_name = [stat_name_ifs(list_stats[0])]
            return column_name
        else:
            list_of_columns = [stat_name_ifs(term) for term in list_stats]
            if 'Invalid' in list_of_columns:
                return 'Invalid'
            else:
                return list_of_columns

    elif words_and_numbs == True:
        items_to_assess = ' '.join(stats).split(', ')

        list_stats = [item.rsplit(' ', 1)[0] for item in items_to_assess]
        values_list = [item.split(' ')[-1] for item in items_to_assess]

        for item in values_list:
            try:
                int(item)
            except:
                return 'Invalid'

        if int(len(list_stats)) == 1:
            column_name = [stat_name_ifs(list_stats[0])]
            if column_name == 'Invalid':
                return 'Invalid'
            else:
                return column_name, values_list
        else:
            list_of_columns = [stat_name_ifs(term) for term in list_stats]
            if 'Invalid' in list_of_columns:
                return 'Invalid'
            else:
                return list_of_columns, values_list


#### ----------------------------------------------------------

