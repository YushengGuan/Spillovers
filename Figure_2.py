import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


RE = ['Wind', 'Solar']
scn_name = ["tfp0_share", "tfp1_share", "tfp2_share", "tfp1_shareHCP", "tfp2_shareHCP"]
scns = ["SCN0", "SCN1:GwC", "SCN1:TwC", "SCN2:GwC", "SCN2:TwC"]
colors = ['darkgrey', 'orangered', 'steelblue']

result_dir = r'CGEresults/'
plt.rcParams['font.family'] = 'Arial'

plt.figure(figsize=(14, 12))#设置图片大小
grid = plt.GridSpec(6, 5, wspace=1.2, hspace=0.6, top=0.95, bottom=0.05, left=0.1, right=0.95)
ax1 = plt.subplot(grid[0:2, :])
width = 0.2
x0 = [1, 5]
plt.xlim(0, 8)
for i in range(len(scn_name)):
    scn = scn_name[i]
    df = pd.read_csv(result_dir + 'res_energy_{}.csv'.format(scn))
    val2030 = df[(df['year']==2030) & (df['unit']=='million toe') & (df['subsector'].isin(RE))]['value'].values
    val2022 = df[(df['year']==2022) & (df['unit']=='million toe') & (df['subsector'].isin(RE))]['value'].values
    RE2030, RE2022 = round(sum(val2030), 2) * 0.041868, round(sum(val2022), 2) * 0.041868  # unit EJ
    if scns[i][-3] == 'T':
        alpha = 0.7
    else:
        alpha = 1
    plt.bar(x0[0], RE2022, width=width, label=scns[i], color=colors[int(scns[i][3])], alpha=alpha)
    plt.bar(x0[1], RE2030, width=width, color=colors[int(scns[i][3])], alpha=alpha)
    x0[0] += width
    x0[1] += width
    print('-'*10, scn, '-'*10)
    print('2030年RE：', round(sum(val2030), 2), '2022年RE：',  round(sum(val2022), 2))
    print('2030年RE是基准请景2022年RE的倍数：',round(sum(val2030)/364.66, 2))
plt.text(-0.6, 70*1.025, 'a.', fontsize=25, fontweight='bold')
# GWC: [0.065, 3.05], [0.06, 3.02], [0.055, 2.99], [0.057, 3.0]
# TwC: [0.073, 3.05], [0.07, 3.03], [0.06, 2.98], [0.062, 2.99], [0.063, 2.99], [0.065, 3.0]
plt.xticks([1.4, 5.4], ['2022', '2030'])
plt.ylabel('RE consumption (EJ)', labelpad=5, fontsize=12)
plt.xlabel('Year', fontsize=12, labelpad=0)
plt.yticks(np.linspace(0, 50, 6), range(0, 51, 10))
plt.ylim(0, 70)
# plt.legend(bbox_to_anchor=(0.85, -0.1), borderaxespad=0, ncol=5, fontsize=10)
plt.legend(loc='upper left', ncols=2, fontsize=10, frameon=False)

ax2 = ax1.twinx()
x2 = np.linspace(1, 5, 9)
for i in range(len(scn_name)):
    scn = scn_name[i]
    df = pd.read_csv(result_dir + 'res_energy_{}.csv'.format(scn))
    ratio = []
    val2022 = 364.66
    for j in range(2022, 2031):
        val = df[(df['year']==j) & (df['unit']=='million toe') & (df['subsector'].isin(RE))]['value'].values
        ratio.append(round(sum(val) / val2022, 2))
    if scns[i][-3] == 'T':
        alpha = 0.7
    else:
        alpha = 1
    plt.plot(x2, ratio, color=colors[int(scns[i][3])], alpha=alpha, marker='.')
    x2 += [width for _ in range(9)]
plt.ylim(0, 3.5)
plt.yticks(np.linspace(1, 3, 5), ['1', '1.5', '2', '2.5', '3'])
plt.hlines(y=1, xmin=1, xmax=10, colors='forestgreen', linestyles='--')
plt.hlines(y=3, xmin=5, xmax=10, colors='forestgreen', linestyles='--')
plt.ylabel('Ratio of 2030 on 2022', labelpad=10, fontsize=12)


def cum_saving(reduction, capacity):
    saving = np.array([0]*len(reduction), dtype=float)
    for t, red in enumerate(reduction):
        saving[t] = red * capacity[t] + saving[t-1]  # unit: million $
    return saving


finalsavings = [0, 0]

df_co = pd.read_excel(r'./Results/Reg_result_solar.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
co_effs = df_co['Global'].values

data_solar = pd.read_excel('Dataset.xlsx', sheet_name='Capacity_solar')
qt0_solar = data_solar['qt0'].values
qt1_solar = data_solar['qt1'].values
qt2_solar = data_solar['qt2'].values
price_si = data_solar['price_si'].values
capa = np.append(data_solar['Global'].values, qt0_solar[-1]*2)
q2030 = np.append(qt0_solar, qt0_solar[-1]*3)
y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
red1 = np.append(y_1 - y_0, (y_1 - y_0)[-1])
red2 = np.append(y_2 - y_0, (y_2 - y_0)[-1])
y = cum_saving(red1, capa)
y1 = cum_saving(red2, capa)
finalsavings[0] += y[-1]
finalsavings[1] += y1[-1]

ax1 = plt.subplot(grid[2:4, 0:3])
x = np.linspace(2011, 2030, 20)
x1 = np.append(np.linspace(2011, 2022, 12), 2030)
x2 = np.append(np.linspace(1, 12, 12), 20)
x1labels = ["'"+str(t)[2:4] if t<=2022 else "" for t in x][:12]
x1labels.append("'30E")
print(x1)
print(x1labels)
xlabels = ["'"+str(t)[2:4] if t<=2022 else "" for t in x][:-1]
xlabels.append("'30E")

x = np.arange(len(x)) + 1
print(x)
# 设置柱与柱之间的宽度
width = 0.3
lns1 = ax1.bar(x[:12], y[:12], width, alpha=0.9, label="GwC scenario", color='#FF9232')
lns2 = ax1.bar(x[:12] + width, y1[:12], width, alpha=0.9, label="TwC scenario", color='#2EA12E')
plt.bar(x[-1], y[-1], width, alpha=0.9, color='#FF9232',
        edgecolor='k', linestyle='dashed')
plt.bar(x[-1] + width, y1[-1], width, alpha=0.9, color='#2EA12E',
        edgecolor='k', linestyle='dashed')
# 将坐标设置在指定位置
plt.xticks(x2+width/2, x1labels)
plt.yticks(np.linspace(0, 10**6, 6), range(0, 1001, 200))
plt.ylabel('Savings (billion USD)')
plt.text(0, 1.05*10**6, 'Solar PV')
plt.text(18.8, 0.55*10**6, int(y[-1]/10**3))
plt.text(19.5, 0.9*10**6, int(y1[-1]/10**3))
ax2 = ax1.twinx()
x3 = x2+width/2
lns3, = ax2.plot(x3[:-1], q2030[1:13], color='k', marker='.', label='Cumulative installed capacity')
ax2.plot(x3[-2:], q2030[12:], color='k', marker='.', linestyle=':')
ax2.set_ylim(0, 4*10**3)
ax2.set_yticks(np.linspace(0, 4*10**3, 5), range(0, 5, 1))
lns = [lns1, lns2, lns3]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper left', frameon=False)
plt.text(-3, 4*10**3*1.05, 'b.', fontsize=25, fontweight='bold')
# plt.legend(loc="upper left")


df_co = pd.read_excel(r'./Results/Reg_result_wind.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
co_effs = df_co['Global'].values

data_wind = pd.read_excel('Dataset.xlsx', sheet_name='Capacity_wind')
qt0_wind = data_wind['qt0'].values
qt1_wind = data_wind['qt1'].values
qt2_wind = data_wind['qt2'].values
capa = np.append(data_wind['Global'].values, qt0_wind[-1]*2)
q2030 = np.append(qt0_wind, qt0_wind[-1]*3)
y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
red1 = np.append(y_1 - y_0, (y_1 - y_0)[-1])
red2 = np.append(y_2 - y_0, (y_2 - y_0)[-1])
y = cum_saving(red1, capa)
y1 = cum_saving(red2, capa)
finalsavings[0] += y[-1]
finalsavings[1] += y1[-1]
ax1 = plt.subplot(grid[4:6,0:3])
x = np.arange(len(x)) + 1
# 设置柱与柱之间的宽度
width = 0.3
lns1 = plt.bar(x[:12], y[:12], width, alpha=0.9, label="GwC scenario", color='#FF9232')
lns2 = plt.bar(x[:12] + width, y1[:12], width, alpha=0.9, label="TwC scenario", color='#2EA12E')
plt.bar(x[-1], y[-1], width, alpha=0.9, color='#FF9232',
        edgecolor='k', linestyle='dashed')
plt.bar(x[-1] + width, y1[-1], width, alpha=0.9, color='#2EA12E',
        edgecolor='k', linestyle='dashed')
# 将坐标设置在指定位置
plt.xticks(x2+width/2, x1labels)
plt.ylabel('Savings (billion USD)')
plt.xlabel('Year')
plt.yticks(np.linspace(0, 0.6*10**6, 7), range(0, 601, 100))
plt.text(0, 1.05*0.6*10**6, 'Wind power')
plt.text(18.8, 0.3*10**6, int(y[-1]/10**3))
plt.text(19.5, 0.55*10**6, int(y1[-1]/10**3))
ax2 = ax1.twinx()
x3 = x2+width/2
lns3, = ax2.plot(x3[:-1], q2030[1:13], color='k', marker='.', label='Cumulative installed capacity')
ax2.plot(x3[-2:], q2030[12:], color='k', marker='.', linestyle=':')
ax2.set_ylim(0, 3*10**3)
ax2.set_yticks(np.linspace(0, 3*10**3, 4), range(0, 4, 1))
ax2.set_ylabel('Cumulative installed capacity (TW)', y=1.15)
lns = [lns1, lns2, lns3]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper left', frameon=False)
plt.text(-3, 3*10**3*1.05, 'c.', fontsize=25, fontweight='bold')
# plt.legend(loc="upper left")

plt.subplot(grid[2:6,3:])
plt.ylabel('Annual investment demand of renewable energy (bn USD)')
fidemand = 1300
finow = 486
width=0.15
start=0.3
plt.xlim(0, 2)
plt.ylim(0, 1600)
print('finalsavings:', finalsavings)
finalsavings = np.array(finalsavings)
finalsavings /= 10**3 * 8  # unit: billion, annually
plt.bar(start, finow, width, alpha=0.9, label='Existing level', color='#2178B5', edgecolor='k')
plt.bar(start, fidemand-finow, width, alpha=0.9, label="Investment gap,\nIRENA forecasted", color='grey',
        bottom=finow, edgecolor='k', linestyle='dashed')
plt.bar(start, finalsavings[0], width, alpha=0.9, label="GwC scenario", color='#FF9232',
        bottom=fidemand, edgecolor='k', linestyle='dashed')
plt.bar(start+width, finow, width, alpha=0.9, color='#2178B5', edgecolor='k')
plt.bar(start+width, fidemand-finow, width, alpha=0.9, color='grey',
        bottom=finow, edgecolor='k', linestyle='dashed')
plt.bar(start+width, finalsavings[1], width, alpha=0.9, label="TwC scenario", color='#2EA12E',
        bottom=fidemand, edgecolor='k', linestyle='dashed')
plt.vlines(0.7, ymin=finow, ymax=fidemand, color='#FF9232')
plt.vlines(0.9, ymin=finow, ymax=fidemand, color='#2EA12E')
plt.text(0.7, 1330, 'gap=0%')
plt.text(0.7, 430, 'gap=100%')
plt.vlines(1.1, ymin=fidemand, ymax=fidemand+finalsavings[0], color='#FF9232', linestyles='dashed')
plt.vlines(1.3, ymin=fidemand, ymax=fidemand+finalsavings[1], color='#2EA12E', linestyles='dashed')
plt.text(1.1, 1250, '\u0394'+'gap={}%'.format(int(finalsavings[0]/fidemand*100)))
plt.text(1.4, 1350, '\u0394'+'gap={}%'.format(int(finalsavings[1]/fidemand*100)))
plt.xticks([])
plt.legend(loc='lower right', frameon=False)
plt.text(-0.5, 1600*1.025, 'd.', fontsize=25, fontweight='bold')

plt.savefig(r'Figs/Figure_2.jpg', dpi=600)
