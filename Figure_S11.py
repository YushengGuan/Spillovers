import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

result_dir = r'CGEinputs/'
plt.rcParams['font.family'] = 'Arial'
df = pd.read_csv(result_dir + 'carbon_price.csv', dtype=float)
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.25, hspace=0.25, left=0.1, right=0.95, top=0.95)
x = np.linspace(1, 14, 14)
gradual = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0])
low = 65
high = 73
for i in range(len(Region)):
    plt.subplot(3, 6, i+1)
    values = df[Region[i]].values[:14]
    plt.plot(x, values, label='SCN0, SCN1', color='forestgreen')
    values_low = np.array(values.copy())
    values_low[6:] += low * gradual
    plt.plot(x, values_low, label='SCN2:GwC', color='steelblue')
    values_high = np.array(values.copy())
    values_high[6:] += high * gradual
    plt.plot(x, values_high, label='SCN2:TwC', color='steelblue', alpha=0.7)
    if i in range(12, 18):
        plt.xticks([1, 4, 7, 14], ["'17", "'20", "'23", "'30"])
    else:
        plt.xticks([], [])
    if i == 6:
        plt.ylabel('Carbon Price (USD/tonne CO$_{2}$', labelpad=10)
    if i == 14:
        plt.xlabel('Year', x=1.05)
plt.legend(bbox_to_anchor=(-1, -0.45), ncol=3, borderaxespad=0., frameon=False)
# ax.remove()
plt.savefig(r'./Figs/Figure_S11.jpg', dpi=300)
