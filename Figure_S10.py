import pandas as pd
import statsmodels.api as sm
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def linear_regression(endog, exog):
    mod = sm.OLS(endog, exog).fit()
    return mod.params, mod.bse, mod.pvalues


def star(pv):
    if pv < 0.001:
        return '***'
    if pv < 0.01:
        return '**'
    if pv < 0.05:
        return '*'
    else:
        return ''


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

year = list(range(2015, 2024))
year2 = list(range(2024, 2031))
t = np.linspace(1, 9, 9)
t2 = np.linspace(10, 16, 7)
values = [[[0 for _ in range(len(ElecType))] for _ in range(len(Region))] for _ in range(len(year2))]
ps = [[0 for _ in range(len(Region))] for _ in range(len(ElecType))]
for region in Region:
    print('-' * 250)
    print(region)
    for Ec in range(len(ElecType)):
        print(ElecType[Ec])
        series = []
        for yr in year:
            df = pd.read_excel('CGEinputs\\ElecTreat_ratio.xls', sheet_name=str(yr))[1:]
            series.append(df[region].iloc[Ec])
        print(f'历史数据: {series}')
        hist = np.array(series)
        c, se, p = linear_regression(hist, sm.add_constant(t))
        print(f'回归结果显著性：{star(p[1])}')
        pred = np.array(t2) * c[1] + c[0]
        print(f'预测数据: {pred}')
        for j in range(len(pred)):
            if pred[j] <= 0:
                values[j][Region.index(region)][Ec] = 0
            else:
                values[j][Region.index(region)][Ec] = pred[j]
        print(p[1], type(p[1]), float(p[1]), type(float(p[1])), c[1])
        if float(c[1]) == 0:
            print(region, Ec)
            ps[Ec][Region.index(region)] = 1
        else:
            ps[Ec][Region.index(region)] = float(p[1])


stars = [['' for _ in range(len(Region))] for _ in range(len(ElecType))]
for i in range(len(ElecType)):
    for j in range(len(Region)):
        stars[i][j] = star(ps[i][j])
stars = np.array(stars)
# 创建 DataFrame
df = pd.DataFrame(ps, columns=Region, index=ElecType)
# 制作热力图
plt.subplots(1, 1, figsize=(12, 8))
plt.subplots_adjust(bottom=0.4, right=0.9)
sns.set(font_scale=1)  # 设置字体比例
# custom_colors = sns.diverging_palette(20, 220, n=256, as_cmap=True)  # 创建自定义的调色板
# 设置横轴和纵轴标签
plt.xlabel('adv_eps', fontsize=20)  # 设置标签字体大小
plt.ylabel('adv_lr', fontsize=20)
# heatmap = sns.heatmap(df, annot=True, cmap='YlGnBu', fmt='.1f')  # 保留一位小数
heatmap = sns.heatmap(df, annot=stars, cmap='Purples_r', alpha=0.8, fmt='', vmin=0, vmax=1)
# 设置横轴和纵轴标签
plt.xlabel('Region', fontsize=10)
plt.ylabel('Electricity type', fontsize=10)
plt.grid(False)
plt.savefig(r"./Figs/Figure_S10.jpg", dpi=300)
