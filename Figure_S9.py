import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

x = list(range(2000, 2031))
fig, ax = plt.subplots(figsize=(15, 8), frameon=False)
fig.subplots_adjust(hspace=0.4, wspace=0.3, bottom=0.15)
colors = ['black', 'grey', 'darkred', 'darkviolet', 'royalblue', 'lightskyblue', 'darkorange', 'palegreen']
for i in range(len(Region)):
    plt.subplot(3, 6, i+1)
    plt.title(Region[i], fontsize=10)
    for j in range(len(ElecType)):
        print(f'正在处理{Region[i]}的{ElecType[j]}'+'-'*20)
        y = []
        for k in range(len(x)):
            if x[k] <= 2023:
                df = pd.read_excel(r'./CGEinputs/ElecTreat_ratio.xls', sheet_name=str(x[k]))
            else:
                df = pd.read_excel(r'./CGEinputs/ElecTreat_ratio_predicted.xls', sheet_name=str(x[k]))
            y.append(df.iloc[j+1, i+1])
        plt.plot(x[:24], y[:24], color=colors[j], label=ElecType[j])
        plt.plot(x[24:], y[24:], color=colors[j], linestyle='dashed')
    if i == 6:
        plt.ylabel('Electricity generation share by technology', labelpad=20)
    if i == 14:
        plt.xlabel('Year', labelpad=2, x=1.2)
    # plt.xticks(np.linspace(2000, 2030, 7), ["'00", "'05", "'10", "'15", "'20", "'25", "'30"])
    plt.xticks([2000, 2010, 2023, 2030], ["'00", "'10", "'23", "'30E"])
    plt.ylim(0, 1)
    plt.yticks(np.linspace(0, 1, 5), ['0', '0.25', '0.5', '0.75', '1'])
plt.legend(bbox_to_anchor=(-1.2, -0.3), ncol=4, borderaxespad=0., frameon=False)
# ax.remove()
plt.savefig(r'./Figs/Figure_S9.jpg', dpi=300)
