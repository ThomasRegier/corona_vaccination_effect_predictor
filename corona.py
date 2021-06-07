import pandas as pd
from assumptions import population, risk_reductions, vacs


vac_list = [f(vac) for vac in vacs for f in (lambda x: x + '_1',lambda x: x + '_2')]


risk_red_1st = [risk_reductions[x-1] for x in [1,3,5,7]]
risk_red_total = [risk_reductions[x-1] + risk_reductions[x] for x in [1,3,5,7]]


risk_reduction_dict = {}
for i, vac in enumerate(vac_list):
    risk_reduction_dict[vac] = risk_reductions[i]

vac_list_cum = [vac+'_cum' for vac in vac_list]
vac_list_2_cum = [vac+'_2_cum' for vac in vacs]

def calc_effects(df,shift = 14):
    df['johnson_2_cum'] = df['johnson_1_cum']
    df['net_effect'] = df[vac_list_cum].shift(shift).dot(risk_reductions)
    df['net_effect_2nd'] = df[vac_list_2_cum].shift(shift).dot(risk_red_total) + (df[vac_list_2_cum].shift(0) - df[vac_list_2_cum].shift(shift)).dot(risk_red_1st)
    df['rel_net_effect'] = df['net_effect'] / population
    #df['rel_net_effect_2nd'] = df['net_effect'] / population
    df['net_effect_after_14'] = df[vac_list_cum].dot(risk_reductions)
    df['rel_net_effect_after_14'] = df['net_effect_after_14'] / population
    for vac in vacs:
        df['rel_' + vac + '_14'] = (df[vac + '_1_cum'] * risk_reduction_dict[vac + '_1']
                                         + df[vac + '_2_cum'] * risk_reduction_dict[vac + '_2']) \
                                        / df['net_effect_after_14']
    df['all_full'] = df[[vac + '_2_cum' for vac in vacs]].sum(axis=1)
    df['all_1'] = df[[vac + '_1_cum' for vac in vacs]].sum(axis=1)
    df['rel_all_1'] = df['all_1'] / population
    df['rel_all_full'] = df['all_full'] / population
    df['R_to_1'] = 1 / (1 - df['rel_net_effect'])
    df['R_to_1_14'] = 1 / (1 - df['rel_net_effect_after_14'])
    df['new_1st'] = df['rel_all_1'] - df['rel_all_1'].shift(1)
    df['new_full'] = df['rel_all_full'] - df['rel_all_full'].shift(1)
    try:
        df['new_total'] = df['new_full'] + df['new_1st'] - (df['johnson_1_cum'] - df['johnson_1_cum'].shift(1))/population
    except:
        df['new_total'] = df['new_full'] + df['new_1st'] - df['johnson_1']/population
    return df


