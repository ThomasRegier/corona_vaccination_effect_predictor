import pandas as pd
import numpy as np
from assumptions import population, risk_reductions, vacs, week_delta


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
    if 'rel_all_1' not in df.columns:
        df['all_full'] = df[[vac + '_2_cum' for vac in vacs]].sum(axis=1)
        df['all_1'] = df[[vac + '_1_cum' for vac in vacs]].sum(axis=1)
    else:
        df['all_full'][df['all_full'].isin([0, np.NaN])] = df[[vac + '_2_cum' for vac in vacs]].sum(axis=1)
        df['all_1'][df['all_1'].isin([0, np.NaN])] = df[[vac + '_2_cum' for vac in vacs]].sum(axis=1)
    #df['all_1'] = np.where(df['all_1'] > population, population, df['all_1'])
    #df['all_full'] = np.where(df['all_full'] > population, population, df['all_full'])

    df['rel_all_1'] = df['all_1'] / population
    df['rel_all_full'] = df['all_full'] / population
    df['R_to_1'] = 1 / (1 - df['rel_net_effect'])
    df['R_to_1_14'] = 1 / (1 - df['rel_net_effect_after_14'])
    df['rel_new_1st'] = df['rel_all_1'] - df['rel_all_1'].shift(1)
    df['rel_new_full'] = df['rel_all_full'] - df['rel_all_full'].shift(1)
    try:
        df['rel_new_total'] = df['rel_new_full'] + df['rel_new_1st'] - (df['johnson_1_cum'] - df['johnson_1_cum'].shift(1))/population
    except:
        df['rel_new_total'] = df['rel_new_full'] + df['rel_new_1st'] - df['johnson_1']/population
    return df

def vac_dist_to_1_2(df_week, i, open_1st, open_full, vac):
    vac_2 = min(df_week.iloc[i-1][vac],df_week.iloc[i-week_delta[vac]][vac + '_1'], open_full)
    df_week.at[i,vac + '_2'] = vac_2
    open_full = open_full - vac_2
    df_week.at[i,'open_full'] = open_full
    #print('open_1st, vac1',open_1st, vac_1)
    vac_1 = min(df_week.iloc[i-1][vac] - df_week.at[i,vac + '_2'],open_1st)
    df_week.at[i,vac + '_1'] = vac_1
    open_1st = open_1st - vac_1
    df_week.at[i, 'open_1st'] = open_1st
    #print('open_full, vac_full',open_full, vac_full)
    return df_week, open_1st, open_full
