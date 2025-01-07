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
    if i == 0:
        plt.text(-5, 0, 'b.', fontweight='bold', fontsize=25)
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
plt.savefig(r'./Figs/Figure_5_b.png', dpi=600)


# maps ------------------------------------------------------------------------------------------------------------
def plot_world_map(var_data, ax1, vs, title, tick, camp="RdYlBu"):
    world = gpd.read_file(r'./worldmap_gaode').rename(columns={'NAME_ENG': 'NAME'})
    map_grid = pd.read_csv(r'./worldmap_gaode/map_name.csv')[['SOC', 'RegAgg']]
    world_grid = world.merge(map_grid, on="SOC", how="left").rename(columns={'RegAgg': 'region'})
    world_grid = world_grid.merge(var_data, on="region", how='left')
    print(var_data)
    fig.patch.set_facecolor('white')
    world_grid.plot(
        column='value',
        ax=ax1,
        cmap=camp,
        vmin=vs[0],
        vmax=vs[1],
        missing_kwds={
            "color": "lightgrey",
        },
    )
    ax1.set_axis_off()
    sm = plt.cm.ScalarMappable(cmap=camp)
    sm.set_array([])
    cbar = fig.colorbar(sm, shrink=0.5, ax=ax1, orientation='horizontal', pad=0, extend='both')
    ax1.set_title(title, fontsize=15)
    cbar.set_label('change rate (%)', fontsize=12)
    cbar.set_ticklabels(tick)


def EV_change(df0, df1, Region, Sector):
    def CPI(df=df0):
        output = df[(df['variable'] == 'household consumption') & (df['year'] == 2030)]['value'].values
        price = df[(df['variable'] == 'commodity price') & (df['year'] == 2030)]['value'].values
        if len(output) != len(price):
            return -1
        else:
            cpi = sum(np.array(output) * np.array(price)) / sum(output)
            return cpi

    def utilities(df=df0):
        cons = df[(df['variable'] == 'household consumption') & (df['year'] == 2030)]
        sav = df[(df['variable'] == 'household saving') & (df['year'] == 2030)]
        utilities = [1 for _ in range(len(Region))]
        for i in range(len(Region)):
            cons_r = cons[cons['region'] == Region[i]]['value'].values
            sav_r = cons[cons['region'] == Region[i]]['value'].values
            share = [cons_r[j] / sum(cons_r) for j in range(len(Sector))]
            # print('sum share:', sum(share))
            # mp_s = sum(sav_r) / (sum(sav_r) + sum(cons_r))
            # mp_c = np.array(share) * (1 - mp_s)
            # print('sum mp_c', sum(mp_c))
            for j in range(len(Sector)):
                utilities[i] *= cons_r[j] ** share[j]
            # utilities[i] *= (sum(sav_r) / CPI(df)) ** mp_s
        return utilities

    utilities0 = utilities(df0)
    utilities1 = utilities(df1)
    EV_c = np.array(utilities1) / np.array(utilities0) - 1
    return EV_c

config = {
    'font.family': 'serif',
    'font.size': 14,
    'mathtext.fontset': 'stix',
    'font.serif': 'Arial'
}
rcParams.update(config)
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(figsize=(15, 8), ncols=2, nrows=2)
plt.subplots_adjust(hspace=0.2, wspace=-0.2, left=0, right=1, bottom=0.05, top=0.95)

# Real GDP ----------------------------------------------------------------------------------------------------
impact2 = pd.read_csv(result_dir + 'res_economy_tfp1_share.csv')['value'].values - \
          pd.read_csv(result_dir + 'res_economy_tfp0_share.csv')['value'].values
df0 = pd.read_csv(result_dir + 'res_economy_tfp0_share.csv')
df2 = df0.copy()
df2['value'] = impact2

data2 = df2[(df2['variable'] == 'real GDP') & (df2['year'] == 2030)]
data0 = df0[(df0['variable'] == 'real GDP') & (df0['year'] == 2030)]
d = data2.groupby(['region'])['value'].sum().reset_index()
d0 = data0.groupby(['region'])['value'].sum().reset_index()
y = d.copy()
y['value'] = d['value'] / d0['value'] * 100
print(f"global gdp loss, {d['value'].sum()} billion, {d['value'].sum() / d0['value'].sum() * 100}%")
plot_world_map(y, axes[0, 0], [-0.5, 0], 'Real GDP, SCN1:GwC', [-0.5, -0.4, -0.3, -0.2, -0.1, 0])

# Household welfare ----------------------------------------------------------------------------------------------------
df0 = pd.read_csv(result_dir + 'res_economy_tfp0_share.csv')
df2 = pd.read_csv(result_dir + 'res_economy_tfp1_share.csv')
ev_change = EV_change(df0, df2, Region, Sector)
y = pd.DataFrame(columns=['region', 'value'])
y['region'] = Region
y['value'] = np.array(ev_change) * 100
y = y.groupby(['region'])['value'].sum().reset_index()
plot_world_map(y, axes[0, 1], [-0.4, 0.1], 'Household welfare, SCN1:GwC', [-0.4, -0.3, -0.2, -0.1, 0, 0.1], camp="RdYlBu")

# Real GDP ----------------------------------------------------------------------------------------------------
impact2 = pd.read_csv(result_dir + 'res_economy_tfp1_shareHCP.csv')['value'].values - \
          pd.read_csv(result_dir + 'res_economy_tfp0_share.csv')['value'].values
df0 = pd.read_csv(result_dir + 'res_economy_tfp0_share.csv')
df2 = df0.copy()
df2['value'] = impact2

data2 = df2[(df2['variable'] == 'real GDP') & (df2['year'] == 2030)]
data0 = df0[(df0['variable'] == 'real GDP') & (df0['year'] == 2030)]
d = data2.groupby(['region'])['value'].sum().reset_index()
d0 = data0.groupby(['region'])['value'].sum().reset_index()
y = d.copy()
y['value'] = d['value'] / d0['value'] * 100
print(f"global gdp loss, {d['value'].sum()} billion, {d['value'].sum() / d0['value'].sum() * 100}%")
plot_world_map(y, axes[1, 0], [-2, 0], 'Real GDP, SCN2:GwC', [-2, -1.6, -1.2, -0.8, -0.4, 0])

# Household welfare ----------------------------------------------------------------------------------------------------
df2 = pd.read_csv(result_dir + 'res_economy_tfp1_shareHCP.csv')
df0 = pd.read_csv(result_dir + 'res_economy_tfp0_share.csv')
ev_change = EV_change(df0, df2, Region, Sector)
y = pd.DataFrame(columns=['region', 'value'])
y['region'] = Region
y['value'] = np.array(ev_change) * 100
# print(y)

y = y.groupby(['region'])['value'].sum().reset_index()
plot_world_map(y, axes[1, 1], [-3, 0], 'Household welfare, SCN2:GwC', [-3, -2.4, -1.8, -1.2, -0.6, 0], camp="RdYlBu")

plt.text(-670, 360, 'a.', fontsize=25, fontweight='bold')
plt.savefig(r'./Figs/Figure_5_a.png', dpi=600)

# Generate figure 5
fig, ax = plt.subplots(figsize=(15, 16), frameon=False)
grid = plt.GridSpec(2, 1, left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplot(grid[0, :])
plt.imshow(plt.imread('Figs/Figure_5_a.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.subplot(grid[1, :])
plt.imshow(plt.imread('Figs/Figure_5_b.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.savefig('Figs/Figure_5.jpg', dpi=600)
