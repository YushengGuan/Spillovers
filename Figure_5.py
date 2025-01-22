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

plt.text(-650, 360, 'a.', fontsize=25, fontweight='bold')
plt.text(-200, 360, 'b.', fontsize=25, fontweight='bold')
plt.text(-650, 100, 'c.', fontsize=25, fontweight='bold')
plt.text(-200, 100, 'd.', fontsize=25, fontweight='bold')
plt.savefig(r'./Figs/Figure_5.jpg', dpi=600)
