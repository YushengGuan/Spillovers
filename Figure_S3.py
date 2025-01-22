import pandas as pd
import matplotlib.pyplot as plt

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

# Emissions plot
impact2 = pd.read_csv(result_dir+'res_emissions_tfp2_share.csv')['value'].values - pd.read_csv(result_dir+'res_emissions_tfp0_share.csv')['value'].values
impact1 = pd.read_csv(result_dir+'res_emissions_tfp1_share.csv')['value'].values - pd.read_csv(result_dir+'res_emissions_tfp0_share.csv')['value'].values
df0 = pd.read_csv(result_dir+'res_emissions_tfp0_share.csv')
df1, df2 = df0.copy(), df0.copy()
df1['value'] = impact1
df2['value'] = impact2
impacts = [df1, df2]
x = list(range(2017, 2031))
fig, ax = plt.subplots(figsize=(15, 5), frameon=False)
fig.subplots_adjust(hspace=0.4, wspace=0.45, bottom=0.15, left=0.05, right=0.95, top=0.95)
# colors = ['black', 'grey', 'darkred', 'darkviolet', 'royalblue', 'lightskyblue', 'darkorange', 'palegreen']
colors = ['lightskyblue', 'darkorange']
colors_scn = ['orangered','orangered', 'steelblue', 'steelblue']
scn_names = ['SCN1:GwC-SCN0', 'SCN1:TwC-SCN0', 'SCN2:GwC-SCN0', 'SCN2:TwC-SCN0']
for i in range(len(Region)):
    plt.subplot(3, 6, i+1)
    plt.title(RegionSimple[i], fontsize=10)
    for j in range(len(impacts)):
        y = []
        for k in range(len(x)):
            y.append(sum(impacts[j][(impacts[j]['region'] == Region[i]) & (impacts[j]['species'] == 'CO2') & (impacts[j]['year'] == x[k])]['value'].values))
        if j in [0, 2, 4]:
            plt.plot(x, y, color=colors_scn[j], label=scn_names[j])
        else:
            plt.plot(x, y, color=colors_scn[j], alpha=0.7, label=scn_names[j])
        plt.scatter(x[0], y[0], color=colors_scn[j], marker='.', alpha=0.7 if j == 1 else 1)
        plt.scatter(x[3], y[3], color=colors_scn[j], marker='.', alpha=0.7 if j == 1 else 1)
        plt.scatter(x[8], y[8], color=colors_scn[j], marker='.', alpha=0.7 if j == 1 else 1)
        plt.scatter(x[13], y[13], color=colors_scn[j], marker='.', alpha=0.7 if j == 1 else 1)
    if i == 6:
        plt.ylabel('Change of CO$_{2}$ emissions (million tonnes)', labelpad=10, fontsize=12)
    if i == 14:
        plt.xlabel('Year', labelpad=2, x=1.2)
    if i in range(12, 18):
        plt.xticks([2017, 2020, 2025, 2030], ["'17", "'20", "'25", "'30"])
    else:
        plt.xticks([], [])
plt.legend(bbox_to_anchor=(-2, -0.45), ncol=4, borderaxespad=0., frameon=False)
# ax.remove()
plt.savefig(r'./Figs/Figure_S3.jpg', dpi=600)
