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

plt.rcParams['font.family'] = 'Arial'
x = np.linspace(10, 22, 13)
xticks = np.linspace(10, 22, 7)
xlabels = ["'10", "'12", "'14", "'16", "'18", "'20", "'22"]
xlabels2 = ["2010", "2012", "2014", "2016", "2018", "2020", "2022"]
cmap = {'Australia': 'darkorange', 'France': 'mediumpurple', 'Germany': 'saddlebrown',
        'India': 'olive', 'Italy': 'forestgreen', 'Japan': 'khaki', 'South Korea': 'pink', 'Spain': 'aqua',
                 'United Kingdom': 'lightgreen', 'United States': 'steelblue', 'China': 'firebrick',
        'Denmark': 'royalblue', 'Sweden': 'chocolate', 'Canada':  'hotpink', 'Turkey': 'bisque', 'Brazil': 'darkgreen',
        'Others': 'grey'}

# Global total installed cost
df_co = pd.read_excel(f'Results\\Reg_result_solar.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
co_effs = df_co['Global'].values
y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
print(f'Global, GwC, Solar, lowered {y_1-y_0}')
print(f'Global, TwC, Solar, lowered {y_2-y_0}')
df_co = pd.read_excel(f'Results\\Reg_result_wind.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
co_effs = df_co['Global'].values
y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
print(f'Global, GwC, Wind, lowered {y_1-y_0}')
print(f'Global, TwC, Wind, lowered {y_2-y_0}')


# total installed cost of solar PV
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.2, hspace=0.3)
df_co = pd.read_excel(f'Results\\Reg_result_solar.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
for i, c in enumerate(country_solar):
    co_effs = df_co[c].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
    print(f'{c}, GwC, Solar, lowered {y_1[-1]-y_0[-1]} in 2022')
    print(f'{c}, TwC, Solar, lowered {y_2[-1]-y_0[-1]} in 2022')
    plt.subplot(3, 4, i+1)
    plt.title(country_solar[i], fontsize=12)
    plt.xticks(xticks, xlabels)
    plt.ylim(0, 10000)
    if i in [0, 4, 8]:
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000], ['0', '2000', '4000', '6000', '8000', '10000'])
    else:
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000], ['', '', '', '', '', ''])
    if i == 4:
        plt.ylabel('Total installed cost (USD/kW)', fontsize=14)
    if i == 0:
        plt.text(4, 10300, 'a.', fontsize=25, fontweight='bold')
    dots = plt.scatter(x, df[c].values, marker='x', label='Observations', color='black')
    plt.plot(x, y_0, label='Global scenario')
    plt.plot(x, y_1, label='GwC scenario')
    plt.plot(x, y_2, label='TwC scenario')
plt.legend(bbox_to_anchor=(2.2, 0.6), borderaxespad=0., frameon=False, fontsize=14)
plt.savefig(f'Figs/Figure_1_a.png', dpi=600)

# total installed cost of wind power
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, wspace=0.2, hspace=0.3)
df_co = pd.read_excel(f'Results\\Reg_result_wind.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
for i, c in enumerate(country_wind):
    co_effs = df_co[c].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
    print(f'{c}, GwC, Wind, lowered {y_1[-1]-y_0[-1]} in 2022')
    print(f'{c}, TwC, Wind, lowered {y_2[-1]-y_0[-1]} in 2022')
    plt.subplot(3, 4, i+1)
    plt.title(country_wind[i], fontsize=12)
    plt.xticks(xticks, xlabels)
    plt.ylim(0, 4000)
    if i in [0, 4, 8]:
        plt.yticks([0, 1000, 2000, 3000, 4000,], ['0', '1000', '2000', '3000', '4000'])
    else:
        plt.yticks([0, 1000, 2000, 3000, 4000], ['', '', '', '', ''])
    if i == 4:
        plt.ylabel('Total installed cost (USD/kW)', fontsize=14)
    if i == 0:
        plt.text(4, 4120, 'b.', fontsize=25, fontweight='bold')
    dots = plt.scatter(x, df[c].values, marker='x', label='Observations', color='black')
    plt.plot(x, y_0, label='Global scenario')
    plt.plot(x, y_1, label='GwC scenario')
    plt.plot(x, y_2, label='TwC scenario')
plt.legend(bbox_to_anchor=(0.5, -0.2), borderaxespad=0., ncol=4, frameon=False, fontsize=14)
plt.savefig(f'Figs/Figure_1_b.png', dpi=600)

country_wind2 = ['Denmark', 'United States', 'Germany', 'Sweden', 'Italy', 'United Kingdom', 'India', 'Spain', 'Canada', 'France', 'Turkey', 'Brazil', 'Others']
country_solar2 = ['Australia', 'France', 'Germany', 'India', 'Italy', 'Japan', 'South Korea', 'Spain', 'United Kingdom', 'United States', 'Others']

# Annual savings of solar PV
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(top=0.95, bottom=0.15, left=0.1, right=0.95, wspace=0.2, hspace=0.1)
df_co = pd.read_excel(f'Results\\Reg_result_solar.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
plt.subplot(2, 1, 1)
plt.xticks(xticks, xlabels2)
plt.ylim(0, 30000)
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_solar2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
    capa = data_solar[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x, capa*(y_1-y_0), bottom=bottom, width=0.8, color=cmap[c])
    bottom += capa*(y_1-y_0)
    print(f'{c}, GwC, Solar, saved {capa*(y_1-y_0)} million USD')
print(f'Total, GwC, Solar, saved {bottom} million USD')
plt.text(9.5, 30000*0.9, 'GwC scenario', fontsize=14)
plt.subplot(2, 1, 2)
plt.xticks(xticks, xlabels2)
plt.ylim(0, 30000)
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_solar2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
    capa = data_solar[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x, capa*(y_2-y_0), bottom=bottom, width=0.8, color=cmap[c], label=country_solar2[i])
    bottom += capa*(y_2-y_0)
    print(f'{c}, TwC, Solar, saved {capa*(y_2-y_0)} million USD')
print(f'Total, TwC, Solar, saved {bottom} million USD')
plt.text(9.5, 30000*0.9, 'TwC scenario', fontsize=14)
plt.ylabel('Annual installed cost savings (million USD)', fontsize=14, y=1.15)
plt.text(7.7, 30000*2.1, 'c.', fontsize=25, fontweight='bold')
plt.legend(bbox_to_anchor=(0.9, -0.1), borderaxespad=0., frameon=False, fontsize=14, ncol=5)
plt.savefig(f'Figs/Figure_1_c.png', dpi=600)

# Annual savings of wind power
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(top=0.95, bottom=0.15, left=0.1, right=0.95, wspace=0.2, hspace=0.1)
df_co = pd.read_excel(f'Results\\Reg_result_wind.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
plt.subplot(2, 1, 1)
plt.xticks(xticks, xlabels2)
plt.ylim(0, 14000)
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_wind2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
    capa = data_wind[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x, capa*(y_1-y_0), bottom=bottom, width=0.8, color=cmap[c])
    bottom += capa*(y_1-y_0)
    print(f'{c}, GwC, Wind, saved {capa*(y_1-y_0)} million USD')
print(f'Total, GwC, Wind, saved {bottom} million USD')
plt.text(9.5, 14000*0.9, 'GwC scenario', fontsize=14)
plt.subplot(2, 1, 2)
plt.xticks(xticks, xlabels2)
plt.ylim(0, 14000)
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_wind2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
    capa = data_wind[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x, capa*(y_2-y_0), bottom=bottom, width=0.8, color=cmap[c], label=country_wind2[i])
    bottom += capa*(y_2-y_0)
    print(f'{c}, TwC, Wind, saved {capa*(y_2-y_0)} million USD')
print(f'Total, TwC, Wind, saved {bottom} million USD')
plt.text(9.5, 14000*0.9, 'TwC scenario', fontsize=14)
plt.ylabel('Annual installed cost savings (million USD)', fontsize=14, y=1.15)
plt.legend(bbox_to_anchor=(0.9, -0.1), borderaxespad=0., frameon=False, fontsize=14, ncol=5)
plt.text(7.7, 14000*2.1, 'd.', fontsize=25, fontweight='bold')
plt.savefig(f'Figs/Figure_1_d.png', dpi=600)

# Generate figure 1
fig, ax = plt.subplots(figsize=(24, 16), frameon=False)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplot(2, 2, 1)
plt.imshow(plt.imread('Figs/Figure_1_a.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.subplot(2, 2, 2)
plt.imshow(plt.imread('Figs/Figure_1_b.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.subplot(2, 2, 3)
plt.imshow(plt.imread('Figs/Figure_1_c.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.subplot(2, 2, 4)
plt.imshow(plt.imread('Figs/Figure_1_d.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.savefig('Figs/Figure_1.jpg', dpi=600)
