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
np.random.seed(42)

plt.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(figsize=(24, 16))
fig.subplots_adjust(hspace=0.2, wspace=0.2, bottom=0.05, top=0.95, left=0.05, right=0.95)
x = np.linspace(10, 22, 13)
xticks = np.linspace(10, 22, 7)
xlabels = ["'10", "'12", "'14", "'16", "'18", "'20", "'22"]

# total installed cost of solar PV
co_solar = pd.read_excel('Results\\Reg_result_solar.xlsx')
co_effs = co_solar['Global'].values
y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
intervals = []  # uncertainty analysis
for item in range(3):
    samples = np.random.normal(co_effs[item], co_effs[item+3], 1000)
    intervals.append(np.percentile(samples, [5, 95]))
y_upper_0 = np.exp(co_effs[0] + intervals[1][1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
y_lower_0 = np.exp(co_effs[0] + intervals[1][0]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
y_upper_1 = np.exp(co_effs[0] + intervals[1][1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
y_lower_1 = np.exp(co_effs[0] + intervals[1][0]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
y_upper_2 = np.exp(co_effs[0] + intervals[1][1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
y_lower_2 = np.exp(co_effs[0] + intervals[1][0]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
df_solar = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
y_real = np.array(df_solar['Global'].values)
plt.subplot(2, 2, 1)
plt.xticks(xticks, xlabels, fontsize=15)
plt.ylim(0, 8000)
plt.yticks([0, 2000, 4000, 6000, 8000], ['0', '2000', '4000', '6000', '8000'], fontsize=15)
# plt.title('Solar PV - total installed cost', fontsize=
plt.text(8, 8300, 'a.', fontweight='bold', fontsize=35)
plt.ylabel('Cost per kW (2022 USD)', fontsize=20)
plt.xlabel('Year', fontsize=20)
plt.plot(x, y_0, label='Global scenario')
plt.plot(x, y_1, label='Gradually without China')
plt.plot(x, y_2, label='Totally without China')
dots = plt.scatter(x, y_real, marker='x', label='Observations', color='black')
plt.plot(x, y_upper_0, alpha=0)
plt.plot(x, y_lower_0, alpha=0)
plt.fill_between(x, y_lower_1, y_upper_1, alpha=0.3, color='#FF9232')
plt.fill_between(x, y_upper_2, y_lower_2, alpha=0.2, color='#2EA12E')
plt.fill_between(x, y_upper_0, y_lower_0, alpha=0.3, color='#2178B5')
plt.legend(loc='upper right', fontsize=20, frameon=False)

# total installed cost of wind power
co_wind = pd.read_excel('Results\\Reg_result_wind.xlsx')
co_effs = co_wind['Global'].values
y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
intervals = []  # uncertainty analysis
for item in range(2):
    samples = np.random.normal(co_effs[item], co_effs[item+2], 1000)
    intervals.append(np.percentile(samples, [5, 95]))
y_upper_0 = np.exp(co_effs[0] + intervals[1][1]*np.log(qt0_wind))
y_lower_0 = np.exp(co_effs[0] + intervals[1][0]*np.log(qt0_wind))
y_upper_1 = np.exp(co_effs[0] + intervals[1][1]*np.log(qt1_wind))
y_lower_1 = np.exp(co_effs[0] + intervals[1][0]*np.log(qt1_wind))
y_upper_2 = np.exp(co_effs[0] + intervals[1][1]*np.log(qt2_wind))
y_lower_2 = np.exp(co_effs[0] + intervals[1][0]*np.log(qt2_wind))
df_wind = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
y_real = np.array(df_wind['Global'].values)
plt.subplot(2, 2, 2)
plt.xticks(xticks, xlabels, fontsize=15)
plt.ylim(0, 4000)
plt.yticks([0, 1000, 2000, 3000, 4000], ['0', '1000', '2000', '3000', '4000'], fontsize=15)
# plt.title('Wind power - total installed cost', fontsize=20)
plt.text(8, 4150, 'b.', fontweight='bold', fontsize=35)
plt.ylabel('Cost per kW (2022 USD)', fontsize=20)
plt.xlabel('Year', fontsize=20)
plt.plot(x, y_0, label='Global scenario')
plt.plot(x, y_1, label='Gradually without China')
plt.plot(x, y_2, label='Totally without China')
dots = plt.scatter(x, y_real, marker='x', label='Observations', color='black')
plt.plot(x, y_upper_0, alpha=0)
plt.plot(x, y_lower_0, alpha=0)
plt.fill_between(x, y_lower_1, y_upper_1, alpha=0.3, color='#FF9232')
plt.fill_between(x, y_upper_2, y_lower_2, alpha=0.2, color='#2EA12E')
plt.fill_between(x, y_upper_0, y_lower_0, alpha=0.3, color='#2178B5')
plt.legend(loc='upper right', fontsize=20, frameon=False)

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
width = 0.3
x = np.linspace(10, 22, 13)
xticks = np.linspace(10, 22, 7)
xlabels = ["'10", "'12", "'14", "'16", "'18", "'20", "'22"]
xlabels2 = ["T G\n2010", "T G\n2012", "T G\n2014", "T G\n2016", "T G\n2018", "T G\n2020", "T G\n2022"]
cmap = {'Australia': 'darkorange', 'France': 'mediumpurple', 'Germany': 'saddlebrown',
        'India': 'olive', 'Italy': 'forestgreen', 'Japan': 'khaki', 'South Korea': 'pink', 'Spain': 'aqua',
                 'United Kingdom': 'lightgreen', 'United States': 'steelblue', 'China': 'firebrick',
        'Denmark': 'royalblue', 'Sweden': 'chocolate', 'Canada':  'hotpink', 'Turkey': 'bisque', 'Brazil': 'darkgreen',
        'Others': 'grey'}


country_wind2 = ['Denmark', 'United States', 'Germany', 'Sweden', 'Italy', 'United Kingdom', 'India', 'Spain', 'Canada', 'France', 'Turkey', 'Brazil', 'Others']
country_solar2 = ['Australia', 'France', 'Germany', 'India', 'Italy', 'Japan', 'South Korea', 'Spain', 'United Kingdom', 'United States', 'Others']

# Annual savings of solar PV
df_co = pd.read_excel(f'Results\\Reg_result_solar.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
plt.subplot(2, 2, 3)
plt.xticks(xticks, xlabels2, fontsize=15)
plt.ylim(0, 30000)
plt.yticks(range(0, 30001, 5000), range(0, 30001, 5000), fontsize=15)
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_solar2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
    capa = data_solar[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x-width/2, capa*(y_1-y_0), bottom=bottom, width=width, color=cmap[c], alpha=0.8, edgecolor='black')
    bottom += capa*(y_1-y_0)
    print(f'{c}, GwC, Solar, saved {capa*(y_1-y_0)} million USD')
print(f'Total, GwC, Solar, saved {bottom} million USD')
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_solar2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
    capa = data_solar[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x+width/2, capa*(y_2-y_0), bottom=bottom, width=width, color=cmap[c], label=country_solar2[i], alpha=0.8, edgecolor='black')
    bottom += capa*(y_2-y_0)
    print(f'{c}, TwC, Solar, saved {capa*(y_2-y_0)} million USD')
print(f'Total, TwC, Solar, saved {bottom} million USD')
# plt.text(9.5, 30000*0.9, 'TwC scenario', fontsize=20)
plt.ylabel('Annual installed cost savings (million USD)', fontsize=20)
plt.text(7.7, 30000*1.05, 'c.', fontsize=35, fontweight='bold')
plt.legend(loc='upper left', borderaxespad=0., frameon=False, fontsize=20, ncol=2)
plt.xlabel('Year', fontsize=20)

# Annual savings of wind power
df_co = pd.read_excel(f'Results\\Reg_result_wind.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
plt.subplot(2, 2, 4)
plt.xticks(xticks, xlabels2, fontsize=15)
plt.ylim(0, 14000)
plt.yticks(range(0, 14001, 2000), range(0, 14001, 2000), fontsize=15)
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_wind2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
    capa = data_wind[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x-width/2, capa*(y_1-y_0), bottom=bottom, width=width, color=cmap[c], alpha=0.8, edgecolor='black')
    bottom += capa*(y_1-y_0)
    print(f'{c}, GwC, Wind, saved {capa*(y_1-y_0)} million USD')
print(f'Total, GwC, Wind, saved {bottom} million USD')
bottom = np.array([0] * len(x), dtype=float)
for i, c in enumerate(country_wind2):
    co_effs = df_co[c].values if c != 'Others' else df_co['Global'].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
    capa = data_wind[c].values  # 2010-2022 annual added capacity, 2010 cumulative
    plt.bar(x+width/2, capa*(y_2-y_0), bottom=bottom, width=width, color=cmap[c], label=country_wind2[i], alpha=0.8, edgecolor='black')
    bottom += capa*(y_2-y_0)
    print(f'{c}, TwC, Wind, saved {capa*(y_2-y_0)} million USD')
print(f'Total, TwC, Wind, saved {bottom} million USD')
plt.ylabel('Annual installed cost savings (million USD)', fontsize=20)
plt.legend(loc='upper left', borderaxespad=0., frameon=False, fontsize=20, ncol=2)
plt.text(7.7, 14000*1.05, 'd.', fontsize=35, fontweight='bold')
plt.xlabel('Year', fontsize=20)

plt.savefig(f'Figs/Figure_1.jpg', dpi=600)
