import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_names(lst1, lst2):
    outcome = []
    for l1 in lst1:
        for l2 in lst2:
            outcome.append(l1+'_'+l2)
    return outcome


Region = [
    "Australia_Oceania",
    "China",
    "Japan",
    "South Korea",
    "Rest of World",
    "Southeast Asia",
    "Central, Western and South Asia",
    "India",
    "Canada",
    "United States",
    "Rest of America",
    "Brazil",
    "EU, UK and EFTA",
    "Eastern Europe",
    "Russia",
    "North Africa",
    "Sub Saharan",
    "South Africa"
]
RegionSimple = ['AUS', 'CHN', 'JPN', 'KOR', 'ROW', 'SEA', 'CWSA', 'IND', 'CAN', 'USA', 'ROA', 'BRA', 'EUE', 'EEU', 'RUS', 'NAF', 'SSH', 'SAF']
ElecType = [
    "Coal_Power",
    "Oil_Power",
    "Gas_Power",
    "Nuclear",
    "Hydro",
    "Wind",
    "Solar",
    "Biomass"
]
Elec_names = ['Coal', 'Oil', 'Gas', 'Nuclear', 'Hydro', 'Wind', 'Solar', 'Biomass']

RE = ['Wind', 'Solar']
Ene = ['Coal', 'Oil', 'Gas', 'Petro', 'Power']

scns = ['SCN0', 'SCN1:GwC', 'SCN1:TwC', 'SCN2:GwC', 'SCN2:TwC']
dfs = ['tfp0_share', 'tfp1_share', 'tfp2_share', 'tfp1_shareHCP', 'tfp2_shareHCP',]
scn_name = ['SCN1:GwC-SCN0', 'SCN1:TwC-SCN0', 'SCN2:GwC-SCN0', 'SCN2:TwC-SCN0']
color_scn = ['darkgrey', 'orangered', 'orangered', 'steelblue', 'steelblue']

result_dir = r'CGEresults/'
plt.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(figsize=(12, 8), frameon=False)
fig.subplots_adjust(hspace=0.4, wspace=0.45, bottom=0.1, left=0.21, top=0.95, right=0.7)
colors_elec = ['black', 'grey', 'darkred', 'darkviolet', 'royalblue', 'lightskyblue', 'darkorange', 'palegreen']
colors_ene = ['dimgrey', 'brown', 'lightsteelblue', 'slategrey', 'darkblue']
scn = scns[0]
width = 0.3
x1 = np.linspace(1, len(Region)+1, len(Region))
x2 = x1 + width
values = np.zeros(len(Region)*(len(Ene)+len(ElecType)))
names = get_names(RegionSimple, Ene+ElecType)
count = 0
for i, region in enumerate(Region):
    df = pd.read_csv(result_dir + 'res_economy_' + dfs[0] + '.csv')
    total = df[(df['variable']=='output')&(df['year']==2030)&(df['region']==region)&(df['sector'].isin(Ene))]['value'].sum()
    # print(f'region:{region}', f'scenario:{scn}', 'energy', 'total', total)
    bots = 0
    for k, e in enumerate(Ene):
        share = df[(df['variable']=='output')&(df['year']==2030)&(df['region']==region)&(df['sector']==e)]['value'].sum()
        # print(f'region:{region}', f'scenario:{scn}', 'energy', 'share', share)
        if i == 0:
            plt.barh(x1[i], share/total, left=bots, height=width, color=colors_ene[k], label=Ene[k])
        else:
            plt.barh(x1[i], share/total, left=bots, height=width, color=colors_ene[k])
        bots += share / total
        values[count] = share/total
        count += 1
    df = pd.read_csv(result_dir + 'res_energy_' + dfs[0] + '.csv')
    total = df[(df['unit']=='million toe')&(df['year']==2030)&(df['region']==region)&(df['subsector'].isin(ElecType))]['value'].sum()
    # print(f'region:{region}', f'scenario:{scn}', 'electricity', 'total', total)
    bots = 0
    for k, e in enumerate(ElecType):
        share = df[(df['unit']=='million toe')&(df['year']==2030)&(df['region']==region)&(df['subsector']==e)]['value'].sum()
        # print(f'region:{region}', f'scenario:{scn}', 'electricity', 'share', share)
        if i == 0:
            plt.barh(x2[i], share/total, left=bots, height=width, color=colors_elec[k], label=ElecType[k])
        else:
            plt.barh(x2[i], share/total, left=bots, height=width, color=colors_elec[k])
        bots += share / total
        values[count] = share/total
        count += 1
plt.yticks(x1+width/2, labels=RegionSimple)
plt.legend(frameon=False, bbox_to_anchor=(1, 0.5))
plt.xticks([0, 0.25, 0.5, 0.75, 1], ['0', '25', '50', '75', '100'])
plt.xlabel('Energy share (%)', fontsize=15)
plt.savefig(r'Figs/Figure_S2.jpg')
