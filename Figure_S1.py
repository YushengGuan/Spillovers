import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


data_solar = pd.read_excel('Dataset.xlsx', sheet_name='Capacity_solar')
qt0_solar = data_solar['qt0'].values
qt1_solar = data_solar['qt1'].values
qt2_solar = data_solar['qt2'].values
price_si = data_solar['price_si'].values
data_wind = pd.read_excel('Dataset.xlsx', sheet_name='Capacity_wind')
qt0_wind = data_wind['qt0'].values
qt1_wind = data_wind['qt1'].values
qt2_wind = data_wind['qt2'].values
names = ['solar', 'wind', 'solar_lcoe', 'wind_lcoe']
country_wind = ['Denmark', 'United States', 'Germany', 'Sweden', 'Italy', 'United Kingdom', 'India', 'Spain', 'Canada', 'France', 'Turkey', 'Brazil']
country_solar = ['Australia', 'France', 'Germany', 'India', 'Italy', 'Japan', 'South Korea', 'Spain', 'United Kingdom', 'United States']

# LCOE of solar PV
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.2, hspace=0.3)
df_co = pd.read_excel(f'Results\\Reg_result_solar_lcoe.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='LCOE_solar')
for i, c in enumerate(country_solar):
    co_effs = df_co[c].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
    x = np.linspace(10, 22, 13)
    xticks = np.linspace(10, 22, 7)
    xlabels = ["'10", "'12", "'14", "'16", "'18", "'20", "'22"]
    plt.subplot(3, 4, i+1)
    plt.title(country_solar[i], fontsize=12)
    plt.xticks(xticks, xlabels)
    plt.ylim(0, 0.8)
    if i in [0, 4, 8]:
        plt.yticks([0, 0.2, 0.4, 0.6, 0.8], ['0', '0.2', '0.4', '0.6', '0.8'])
    else:
        plt.yticks([0, 0.2, 0.4, 0.6, 0.8], ['', '', '', '', ''])
    if i == 4:
        plt.ylabel('LCOE (2022 USD per kWh)', fontsize=14)
    if i == 0:
        plt.text(4, 0.8*1.03, 'a.', fontsize=16, fontweight='bold')
    dots = plt.scatter(x, df[c].values, marker='x', label='Observations', color='black')
    plt.plot(x, y_0, label='Global scenario')
    plt.plot(x, y_1, label='GwC scenario')
    plt.plot(x, y_2, label='TwC scenario')
plt.legend(bbox_to_anchor=(2.2, 0.6), borderaxespad=0., frameon=False, fontsize=14)
plt.savefig('Figs/Figure_S1_a.png', dpi=300)

# LCOE of wind power
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, wspace=0.2, hspace=0.3)
df_co = pd.read_excel(f'Results\\Reg_result_wind_lcoe.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='LCOE_wind')
for i, c in enumerate(country_wind):
    co_effs = df_co[c].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
    x = np.linspace(10, 22, 13)
    xticks = np.linspace(10, 22, 7)
    xlabels = ["'10", "'12", "'14", "'16", "'18", "'20", "'22"]
    plt.subplot(3, 4, i+1)
    plt.title(country_wind[i], fontsize=12)
    plt.xticks(xticks, xlabels)
    plt.ylim(0, 0.2)
    if i in [0, 4, 8]:
        plt.yticks([0, 0.05, 0.1, 0.15, 0.2], ['0', '0.05', '0.1', '0.15', '0.2'])
    else:
        plt.yticks([0, 0.05, 0.1, 0.15, 0.2], ['', '', '', '', ''])
    if i == 4:
        plt.ylabel('LCOE (2022 USD per kWh)', fontsize=14)
    if i == 0:
        plt.text(4, 0.2*1.03, 'b.', fontsize=16, fontweight='bold')
    dots = plt.scatter(x, df[c].values, marker='x', label='Observations', color='black')
    plt.plot(x, y_0, label='Global scenario')
    plt.plot(x, y_1, label='GwC scenario')
    plt.plot(x, y_2, label='TwC scenario')
plt.legend(bbox_to_anchor=(0.5, -0.2), borderaxespad=0., ncol=4, frameon=False, fontsize=14)
plt.savefig('Figs/Figure_S1_b.png', dpi=300)

fig, ax = plt.subplots(figsize=(12, 16), frameon=False)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplot(2, 1, 1)
plt.imshow(plt.imread('Figs/Figure_S1_a.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.subplot(2, 1, 2)
plt.imshow(plt.imread('Figs/Figure_S1_b.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.savefig('Figs/Figure_S1.jpg', dpi=600)
