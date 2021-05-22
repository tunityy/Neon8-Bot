from string import capwords


def column_to_text(column_name):
    if type(column_name) == str:
        return capwords(column_name.replace('_', ' '))
    else:
        results = [capwords(y.replace('_', ' ')) for y in column_name]
        return results


def stat_name_ifs(stat):
    st = str(stat).lower()
    st = st.replace(' ', '')
    st = st.replace('_', '')
    # column_name = ['hunger', 'humanity', 'stains', 'current_willpower', 'total_willpower', 'superficial_damage', 'aggravated_damage', 'health']
    column_name = ['hunger', 'humanity', 'stains', 'health']

    if st in column_name:
        return st
    else:
        # some of these include common or possible typos and misspellings
        hung_synonyms = ['currenthunger', 'currenthung', 'hung', 'hun', 'hungry', 'hungerdice', 'hungdice',
                         'hd', 'bp', 'bloodpool', 'blooddice', 'bd',
                         'hugn', 'hugner', 'hungre', 'curenthunger', 'curenthung', 'bloop', 'blooppool', 'bloopool']

        hum_synonyms = ['hum', 'huemanatee', 'humane', 'human', 'humanty', 'humanit', 'humantiy', 'humanaty']

        stains_synonyms = ['stain', 'stian', 'st', 'stians', 'stans']

        cwp_synonyms = ['currentwillpower', 'willpower', 'wp', 'currentwp', 'will', 'currentwill', 'currentwp', 'cwill', 'cwp', 'cw', 'willp', 'currentwillp', 'cwillp',
                        'wilpower', 'curentwillpower', 'current', 'curentwill', 'wil', 'currentwilpower', 'curentwilpower', 'wpwr', 'willpwr', 'wllpwr', 'wlpwr']

        twp_synonyms = ['totalwillpower', 'totalwp', 'twp', 'total', 'tot', 'totalwill', 'willpowertotal', 'wptotal', 'willtotal', 'twill', 'tw', 'twillp', 'twillpower',
                        'totalwilpower', 'totalwil', 'tote', 'totlewillpower', 'totlwillpower', 'totwill', 't', 'totwil', 'totwp', 'to', 'twil']

        spr_dmg_synonyms = ['superficialdamage', 'superficial', 'superficialdmg', 'sdmg', 'sdamage', 'sdmg', 'super', 'superdmg',
                            'supre', 'superficaldamage', 'superficaldmg', 'superfical', 'superfishul', 'superfishuldamage', 'superfishuldmg']

        agg_dmg_synonyms = ['aggravateddamage', 'agg', 'aggravated', 'aggr', 'aggdmg', 'aggrdmg', 'aggravateddmg', 'aggra', 'aggdamage', 'admg', 'adamage',
                            'aggro', 'aggrivated', 'aggrivateddamage', 'aggrivateddmg', 'aggrevated', 'aggrevateddamage', 'aggrevateddmg', 'aggrovated', 'aggrovateddamage', 'aggrovateddmg', 'aggrovateddmg']

        health_synonyms = ['hp', 'hitpoints', 'healthpoints', 'healthbar', 'life', 'heal'
                           'heath', 'healh', 'helth']

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

### TODO: when it's just a list of one word it actually just comes out as a string. Need to change it to a list?
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

