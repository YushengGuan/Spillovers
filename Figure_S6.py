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
fig, ax = plt.subplots(figsize=(12, 8))
fig.subplots_adjust(hspace=0.3, wspace=0.2, bottom=0.2, top=0.95)
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
plt.xticks(xticks, xlabels)
plt.ylim(0, 8000)
plt.yticks([0, 2000, 4000, 6000, 8000], ['0', '2000', '4000', '6000', '8000'])
# plt.title('Solar PV - total installed cost', fontsize=
plt.text(7, 8300, 'a.', fontweight='bold', fontsize=14)
plt.ylabel('Cost per kW (2022 USD)', fontsize=10)
plt.text(20, 7000, 'lr={:.2f}'.format(1-2**co_effs[1]), fontsize=12)
plt.plot(x, y_0, label='Global scenario')
plt.plot(x, y_1, label='Gradually without China')
plt.plot(x, y_2, label='Totally without China')
dots = plt.scatter(x, y_real, marker='x', label='Observations', color='black')
plt.plot(x, y_upper_0, alpha=0)
plt.plot(x, y_lower_0, alpha=0)
plt.fill_between(x, y_lower_1, y_upper_1, alpha=0.3, color='#FF9232')
plt.fill_between(x, y_upper_2, y_lower_2, alpha=0.2, color='#2EA12E')
plt.fill_between(x, y_upper_0, y_lower_0, alpha=0.3, color='#2178B5')

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
plt.xticks(xticks, xlabels)
plt.ylim(0, 4000)
plt.yticks([0, 1000, 2000, 3000, 4000], ['0', '1000', '2000', '3000', '4000'])
# plt.title('Wind power - total installed cost', fontsize=14)
plt.text(7, 4150, 'b.', fontweight='bold', fontsize=14)
plt.ylabel('Cost per kW (2022 USD)', fontsize=10)
plt.text(20, 3500, 'lr={:.2f}'.format(1-2**co_effs[1]), fontsize=12)
plt.plot(x, y_0, label='Global scenario')
plt.plot(x, y_1, label='Gradually without China')
plt.plot(x, y_2, label='Totally without China')
dots = plt.scatter(x, y_real, marker='x', label='Observations', color='black')
plt.plot(x, y_upper_0, alpha=0)
plt.plot(x, y_lower_0, alpha=0)
plt.fill_between(x, y_lower_1, y_upper_1, alpha=0.3, color='#FF9232')
plt.fill_between(x, y_upper_2, y_lower_2, alpha=0.2, color='#2EA12E')
plt.fill_between(x, y_upper_0, y_lower_0, alpha=0.3, color='#2178B5')

# LCOE of solar PV
co_solar = pd.read_excel('Results\\Reg_result_solar_lcoe.xlsx')
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
df_solar = pd.read_excel('Dataset.xlsx', sheet_name='LCOE_solar')
y_real = np.array(df_solar['Global'].values)
plt.subplot(2, 2, 3)
plt.xticks(xticks, xlabels)
plt.ylim(0, 0.6)
plt.yticks([0, 0.15, 0.3, 0.45, 0.6], ['0', '0.15', '0.3', '0.45', '0.6'])
# plt.title('Solar PV - LCOE', fontsize=14)
plt.text(7, 0.6225, 'c.', fontweight='bold', fontsize=14)
plt.ylabel('LCOE per kWh (2022 USD)', fontsize=10)
plt.text(20, 0.875*0.6, 'lr={:.2f}'.format(1-2**co_effs[1]), fontsize=12)
plt.plot(x, y_0, label='Global scenario')
plt.plot(x, y_1, label='Gradually without China')
plt.plot(x, y_2, label='Totally without China')
dots = plt.scatter(x, y_real, marker='x', label='Observations', color='black')
plt.plot(x, y_upper_0, alpha=0)
plt.plot(x, y_lower_0, alpha=0)
plt.fill_between(x, y_lower_1, y_upper_1, alpha=0.3, color='#FF9232')
plt.fill_between(x, y_upper_2, y_lower_2, alpha=0.2, color='#2EA12E')
plt.fill_between(x, y_upper_0, y_lower_0, alpha=0.3, color='#2178B5')

# LCOE of wind power
co_wind = pd.read_excel('Results\\Reg_result_wind_lcoe.xlsx')
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
df_wind = pd.read_excel('Dataset.xlsx', sheet_name='LCOE_wind')
y_real = np.array(df_wind['Global'].values)
plt.subplot(2, 2, 4)
plt.xticks(xticks, xlabels)
plt.ylim(0, 0.4)
plt.yticks(np.linspace(0, 0.4, 5), ['0', '0.1', '0.2', '0.3', '0.4'])
# plt.title('Wind power - LCOE', fontsize=14)
plt.text(7, 0.415, 'd.', fontweight='bold', fontsize=14)
plt.ylabel('LCOE per kWh (2022 USD)', fontsize=10)
plt.text(20, 0.35, 'lr={:.2f}'.format(1-2**co_effs[1]), fontsize=12)
plt.plot(x, y_0, label='Global scenario')
plt.plot(x, y_1, label='Gradually without China')
plt.plot(x, y_2, label='Totally without China')
dots = plt.scatter(x, y_real, marker='x', label='Observations', color='black')
plt.plot(x, y_upper_0, alpha=0)
plt.plot(x, y_lower_0, alpha=0)
plt.fill_between(x, y_lower_1, y_upper_1, alpha=0.3, color='#FF9232')
plt.fill_between(x, y_upper_2, y_lower_2, alpha=0.2, color='#2EA12E')
plt.fill_between(x, y_upper_0, y_lower_0, alpha=0.3, color='#2178B5')

# ax.remove()
plt.legend(bbox_to_anchor=(0.5, -0.2), borderaxespad=0, fontsize=14, ncols=2, frameon=False)
plt.savefig('Figs\\Figure_S6.jpg', dpi=600)
