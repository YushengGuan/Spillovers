import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

RE = ['Wind', 'Solar']
scn_name = ["tfp0_share", "tfp1_share", "tfp2_share", "tfp1_shareHCP", "tfp2_shareHCP"]
scns = ["SCN0", "SCN1:GwC", "SCN1:TwC", "SCN2:GwC", "SCN2:TwC"]

result_dir = r'CGEresults/'
plt.rcParams['font.family'] = 'Arial'

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

x = list(range(2017, 2031))
fig, ax = plt.subplots(figsize=(16, 8), frameon=False)
fig.subplots_adjust(hspace=0.4, wspace=0.35, bottom=0.15)
colors = ['grey', 'orangered', 'goldenrod', 'forestgreen', 'steelblue', 'mediumpurple', 'pink']
colors = ['forestgreen', 'orangered', 'steelblue']
for i in range(len(Region)):
    plt.subplot(3, 6, i+1)
    plt.title(Region[i], fontsize=10)
    for j in range(len(scn_name)):
        scn = scn_name[j]
        if scns[j][-3] == 'G':
            alpha = 0.7
        else:
            alpha = 1
        df = pd.read_csv(result_dir + 'res_economy_{}.csv'.format(scn))
        y = df[(df['region'] == Region[i]) & (df['variable'] == 'real GDP')]['value'].values
        print(y)
        print(x)
        plt.plot(x, y, color=colors[int(scns[j][3])], label=scns[j])
        # plt.semilogy(x, y, color=colors[int(scns[j][3])], label=scns[j])
    if i == 6:
        plt.ylabel('Real GDP (billion USD)', labelpad=10)
    if i == 14:
        plt.xlabel('Year', labelpad=2, x=1.2)
    plt.xticks([2017, 2020, 2025, 2030], ["'17", "'20", "'25", "'30"])
plt.legend(bbox_to_anchor=(-0.9, -0.3), ncol=5, borderaxespad=0., frameon=False)
# ax.remove()
plt.savefig(r'./Figs/Figure_S8.jpg', dpi=300)
