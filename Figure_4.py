import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

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


# EmissionsMap ----------------------------------------------------------------------------------------------------
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
    

fig, axes = plt.subplots(figsize=(15, 5), ncols=2, nrows=1)
plt.subplots_adjust(hspace=0.2, wspace=0, left=0, right=1, bottom=0.05, top=1)
impact1 = pd.read_csv(result_dir + 'res_emissions_tfp1_share.csv')['value'].values - \
          pd.read_csv(result_dir + 'res_emissions_tfp0_share.csv')['value'].values
impact2 = pd.read_csv(result_dir + 'res_emissions_tfp1_shareHCP.csv')['value'].values - \
          pd.read_csv(result_dir + 'res_emissions_tfp0_share.csv')['value'].values
df0 = pd.read_csv(result_dir + 'res_emissions_tfp0_share.csv')
df1, df2 = df0.copy(), df0.copy()
df1['value'], df2['value'] = impact1, impact2

data1 = df1[(df1['species'] == 'CO2') & (df1['year'] == 2030)]
data2 = df2[(df2['species'] == 'CO2') & (df2['year'] == 2030)]
data0 = df0[(df0['species'] == 'CO2') & (df0['year'] == 2030)]
d1 = data1.groupby(['region'])['value'].sum().reset_index()
d2 = data2.groupby(['region'])['value'].sum().reset_index()
d0 = data0.groupby(['region'])['value'].sum().reset_index()
y1, y2 = d0.copy(), d0.copy()
y1['value'], y2['value'] = d1['value'] / d0['value'] * 100, d2['value'] / d0['value'] * 100
plot_world_map(y1, axes[0], [-0.5, 2], 'CO$_{2}$ emissions, SCN1:GwC', [-0.5, 0, 0.5, 1, 1.5, 2], camp="RdYlBu_r")
plot_world_map(y2, axes[1], [-20, 5], 'CO$_{2}$ emissions, SCN2:GwC', [-20, -15, -10, -5, 0, 5], camp="RdYlBu_r")
# plt.text(-570, 100, 'a.', fontsize=20, fontweight='bold')
plt.savefig(r'Figs/Figure_4_a.png', dpi=600)


# Emissions polar bar
impact1 = pd.read_csv(result_dir+'res_emissions_tfp2_share.csv')['value'].values - pd.read_csv(result_dir+'res_emissions_tfp0_share.csv')['value'].values
df0 = pd.read_csv(result_dir+'res_emissions_tfp0_share.csv')
df1 = df0.copy()
df1['value'] = impact1

x = list(range(18))
# colors = ['black', 'grey', 'darkred', 'darkviolet', 'royalblue', 'lightskyblue', 'darkorange', 'palegreen']
colors = ['lightskyblue', 'darkorange']
colors_scn = ['orangered', 'steelblue']
scn_names = ['SCN1:GwC', 'SCN2:GwC']
Sector_new = ['Agriculture & Forestry', 'Fossil fuels', 'Mine & Manufacture', 'Power', 'Services', 'Transportation']
Sec = [
    ["Rice", "Crops nec", "Bovine cattle, sheep and goats, horses", "Animal products nec", "Forestry"],
    ["Coal", "Oil", "Gas", "Petro"],
    ["Mine", "Manufac"],
    ["Power"],
    ["WatWaste", "OthServ"],
    ["Transport"]
]

fig, axes = plt.subplots(figsize=(15, 10), frameon=False)
fig.subplots_adjust(hspace=0.2, wspace=0, bottom=0.05, top=0.95, left=0.05, right=0.95)
# plt.text(0, 1, 'c.', fontweight='bold', fontsize=15)
bottoms = [-1, -1, -1, -1, -1, -1]
tops = [4, 2, 5, 30, 8, 0]
for i, sec in enumerate(Sector_new):
    ax = plt.subplot(2, 3, i+1, projection='polar')
    plt.title(sec)
    data = np.array([0]*(len(Region)+1), dtype=float)
    for j, region in enumerate(Region):
        y = sum(df1[(df1['sector'].isin(Sec[i])) & (df1['species'] == 'CO2') & (df1['year'] == 2030) & (df1['region'] == region)]['value'].values)
        y0 = sum(df0[(df0['sector'].isin(Sec[i])) & (df0['species'] == 'CO2') & (df0['year'] == 2030) & (df0['region'] == region)]['value'].values)
        data[j+1] = y / y0 * 100
    y_g = sum(df1[(df1['sector'].isin(Sec[i])) & (df1['species'] == 'CO2') & (df1['year'] == 2030)]['value'].values)
    y0_g = sum(df0[(df0['sector'].isin(Sec[i])) & (df0['species'] == 'CO2') & (df0['year'] == 2030)]['value'].values)
    print(f'{sec}, {data}, global mean: {y_g / y0_g * 100}')
    fig.patch.set_alpha(0)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    theta = np.linspace(0, 2*np.pi, len(data), endpoint=False)
    width = 2 * np.pi / (len(data) + 9)
    ax.set_rlim(bottoms[i], tops[i])
    data[0] = bottoms[0]
    ax.bar(theta, data-bottoms[i], width=width, bottom=bottoms[i], color='orangered')
    for k, region in enumerate(RegionSimple):
        plt.text(theta[k+1], data[k+1]+(tops[i]-bottoms[i])*0.15, region, ha='center', va='center',
                    rotation=90-np.rad2deg(theta[k+1]) if theta[k+1] < np.pi else 270 - np.rad2deg(theta[k+1]),
                    rotation_mode='anchor')
    for y in np.linspace(bottoms[i], tops[i], 5):
        plt.plot(np.linspace(-width/2, width/2, 5), [y]*5, color='black', alpha=0.8, linewidth=0.8)
        plt.text(0, y+(tops[i]-bottoms[i])*0.03, str(y)+'%', ha='center', va='center')
    ax.axis('off')
# ax.remove()
plt.savefig(r'Figs/Figure_4_c.png', dpi=600)

# Generate figure 4
fig, ax = plt.subplots(figsize=(15, 15), frameon=False)
grid = plt.GridSpec(3, 1, left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplot(grid[0, :])
plt.imshow(plt.imread('Figs/Figure_4_a.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.text(100/3, 300, 'a.', fontweight='bold', fontsize=25)
plt.text(4500, 300, 'b.', fontweight='bold', fontsize=25)
# plt.subplot(grid[1, :])
# plt.imshow(plt.imread('Figs/Figure_4_b.png'))
# plt.xticks([])
# plt.yticks([])
# plt.axis('off')
# plt.text(100, 80, 'b.', fontweight='bold', fontsize=25)
plt.subplot(grid[1:, :])
plt.imshow(plt.imread('Figs/Figure_4_c.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.text(100/3, 60, 'c.', fontweight='bold', fontsize=25)
plt.text(3000, 60, 'd.', fontweight='bold', fontsize=25)
plt.text(6000, 60, 'e.', fontweight='bold', fontsize=25)
plt.text(100/3, 3000, 'f.', fontweight='bold', fontsize=25)
plt.text(3000, 3000, 'g.', fontweight='bold', fontsize=25)
plt.text(6000, 3000, 'h.', fontweight='bold', fontsize=25)
# ax.remove()
plt.savefig('Figs/Figure_4.jpg', dpi=600)
