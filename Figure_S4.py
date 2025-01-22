import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib import rcParams

RE = ['Wind', 'Solar']
result_dir = r'CGEresults/'
plt.rcParams['font.family'] = 'Arial'

Sector = [
    "Rice",
    "Crops nec",
    "Bovine cattle, sheep and goats, horses",
    "Animal products nec",
    "Forestry",
    "Coal",
    "Oil",
    "Gas",
    "Mine",
    "Manufac",
    "Petro",
    "Power",
    "WatWaste",
    "OthServ",
    "Transport",
]
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
Sector_new = ['Agriculture & Forestry', 'Fossil fuels', 'Mine & Manufacture', 'Power', 'Services', 'Transportation']
Sec = [
    ["Rice", "Crops nec", "Bovine cattle, sheep and goats, horses", "Animal products nec", "Forestry"],
    ["Coal", "Oil", "Gas", "Petro"],
    ["Mine", "Manufac"],
    ["Power"],
    ["WatWaste", "OthServ"],
    ["Transport"]
]

impact1 = pd.read_csv(result_dir+'res_economy_tfp1_share.csv')['value'].values - pd.read_csv(result_dir+'res_economy_tfp0_share.csv')['value'].values
impact2 = pd.read_csv(result_dir+'res_economy_tfp2_share.csv')['value'].values - pd.read_csv(result_dir+'res_economy_tfp0_share.csv')['value'].values
impact3 = pd.read_csv(result_dir+'res_economy_tfp1_shareHCP.csv')['value'].values - pd.read_csv(result_dir+'res_economy_tfp0_share.csv')['value'].values
impact4 = pd.read_csv(result_dir+'res_economy_tfp2_shareHCP.csv')['value'].values - pd.read_csv(result_dir+'res_economy_tfp0_share.csv')['value'].values
df0 = pd.read_csv(result_dir+'res_economy_tfp0_share.csv')
df1, df2, df3, df4, df5, df6 = df0.copy(), df0.copy(), df0.copy(), df0.copy(), df0.copy(), df0.copy()
df1['value'] = impact1
df2['value'] = impact2
df3['value'] = impact3
df4['value'] = impact4
# df5['value'] = impact5
# df6['value'] = impact6
impacts = [df1, df2, df3, df4, df5, df6]

x = np.arange(len(Region))
# colors = ['black', 'grey', 'darkred', 'darkviolet', 'royalblue', 'lightskyblue', 'darkorange', 'palegreen']
colors = ['lightskyblue', 'darkorange']
colors_scn = ['orangered', 'orangered', 'steelblue', 'steelblue']
scn_names = ['SCN1:GwC', 'SCN1:TwC', 'SCN2:GwC', 'SCN2:TwC']
fig, ax = plt.subplots(figsize=(15, 8), frameon=False)
fig.subplots_adjust(hspace=0.4, wspace=0.2, bottom=0.15, top=0.95, left=0.1, right=0.95)
width=0.4
for i in range(len(Sector_new)):
    plt.subplot(4, 3, i+1)
    plt.title(Sector_new[i], fontsize=15)
    for j in range(0, 2):
        y = [0 for _ in range(18)]
        y0 = [0 for _ in range(18)]
        for k in range(len(Region)):
            y[k] = sum(impacts[j][(impacts[j]['sector'].isin(Sec[i])) & (impacts[j]['variable'] == 'output') &
                     (impacts[j]['year'] == 2030) & (impacts[j]['region'] == Region[k])]['value'].values)
            y0[k] = sum(df0[(df0['sector'].isin(Sec[i])) & (df0['variable'] == 'output') &
                     (df0['year'] == 2030) & (df0['region'] == Region[k])]['value'].values)
        ratio = np.array(y) / np.array(y0) * 100
        print(scn_names[j], Sector_new[i], 'value')
        print(np.array(y))
        print(scn_names[j], Sector_new[i], 'ratio')
        print(ratio)
        if j in [0, 2, 4]:
            plt.bar(x, ratio, color=colors_scn[j], label=scn_names[j], width=width)
            # print(scn_names[j])
        else:
            plt.bar(x+width, ratio, color=colors_scn[j], label=scn_names[j], alpha=0.7, width=width)
            # print(scn_names[j])
    if i == 3:
        plt.ylabel('Change of total output by sector (%)', labelpad=5, y=-0.25, fontsize=15)
    plt.xticks([], [], rotation=90, fontsize=5)
plt.legend(bbox_to_anchor=(-0.7, -3.5), ncol=2, borderaxespad=0, frameon=False)
for i in range(len(Sector_new)):
    plt.subplot(4, 3, i+7)
    plt.title(Sector_new[i], fontsize=15)
    for j in range(2, 4):
        y = [0 for _ in range(18)]
        y0 = [0 for _ in range(18)]
        for k in range(len(Region)):
            y[k] = sum(impacts[j][(impacts[j]['sector'].isin(Sec[i])) & (impacts[j]['variable'] == 'output') &
                     (impacts[j]['year'] == 2030) & (impacts[j]['region'] == Region[k])]['value'].values)
            y0[k] = sum(df0[(df0['sector'].isin(Sec[i])) & (df0['variable'] == 'output') &
                     (df0['year'] == 2030) & (df0['region'] == Region[k])]['value'].values)
        ratio = np.array(y) / np.array(y0) * 100
        print(scn_names[j], Sector_new[i], 'value')
        print(np.array(y))
        print(scn_names[j], Sector_new[i], 'ratio')
        print(ratio)
        if j in [0, 2, 4]:
            plt.bar(x, ratio, color=colors_scn[j], label=scn_names[j], width=width)
            # print(scn_names[j])
        else:
            plt.bar(x+width, ratio, color=colors_scn[j], label=scn_names[j], alpha=0.7, width=width)
            # print(scn_names[j])
    if i == 4:
        plt.xlabel('Region', labelpad=5)
    if i in range(3, 6):
        plt.xticks(x, RegionSimple, rotation=90, fontsize=10)
    else:
        plt.xticks([], [], rotation=90, fontsize=5)
plt.legend(bbox_to_anchor=(0.05, -0.7), ncol=2, borderaxespad=0, frameon=False)
# ax.remove()
plt.savefig(r'./Figs/Figure_S4.jpg', dpi=600)
