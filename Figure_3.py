import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def find_top_ten(numbers, names, colors):
    abs_numbers = np.abs(numbers)
    sorted_indices = np.argsort(abs_numbers)[::-1]
    top_10_indices = sorted_indices[:30]
    top_10_numbers = [numbers[_] for _ in top_10_indices]
    top_10_names = np.array(names)[top_10_indices]
    return top_10_numbers, top_10_names, np.array(colors)[top_10_indices]


def get_names(lst1, lst2):
    outcome = []
    for l1 in lst1:
        for l2 in lst2:
            outcome.append(l1+'_'+l2)
    return outcome


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

fig, ax = plt.subplots(figsize=(16, 4), frameon=False)
plt.subplots_adjust(left=0.08, bottom=0.1, right=0.95, top=0.9)
plt.subplot(1,2,1)
x = np.linspace(1, len(Ene)+1, len(Ene))
width=0.15
bots = np.zeros(len(Ene))
for i, scn in enumerate(scns):
    df = pd.read_csv(result_dir + 'res_economy_' + dfs[i] + '.csv')
    for j, e in enumerate(Ene):
        y = df[(df['sector']==e)&(df['variable']=='output')&(df['year']==2030)]['value'].sum()
        print(f'{scn}, {e}, {y}')
        alpha = 0.7 if i in [2, 4] else 1
        if j == 0:
            plt.bar(x[j]+width*i, y-bots[j], color=color_scn[i], width=width, label=scn, bottom=bots[j], alpha=alpha)
        else:
            plt.bar(x[j]+width*i, y-bots[j], color=color_scn[i], width=width, bottom=bots[j], alpha=alpha)
        if i in [1, 3]:
            if int((y-bots[j])/bots[j]*100) <= 0:
                plt.annotate(str(int((y-bots[j])/bots[j]*100))+'%', xy=(x[j]+width*i, bots[j]), ha='center')
            else:
                plt.annotate(str(int((y-bots[j])/bots[j]*100))+'%', xy=(x[j]+width*i, y), ha='center')
        if i == 0:
            bots[j] = y
plt.xticks(x+0.3, labels=Ene)
plt.ylim(0, 4500)
plt.ylabel('Energy consumption (billion USD)', fontsize=12)
plt.legend(frameon=False, loc='upper left')
plt.text(-0.3, 4500*1.01, 'a.', fontsize=25, fontweight='bold')

plt.subplot(1, 2, 2)
x = np.linspace(1, len(ElecType)+1, len(ElecType))
bots = np.zeros(len(ElecType))
for i, scn in enumerate(scns):
    df = pd.read_csv(result_dir + 'res_energy_' + dfs[i] + '.csv')
    for j, e in enumerate(ElecType):
        alpha = 0.7 if i in [2, 4] else 1
        y = df[(df['subsector']==e)&(df['unit']=='million toe')&(df['year']==2030)]['value'].sum() * 0.041868
        print(f'{scn}, {e}, {y}')
        if j == 0:
            plt.bar(x[j]+width*i, y-bots[j], color=color_scn[i], width=width, label=scn, bottom=bots[j], alpha=alpha)
        else:
            plt.bar(x[j]+width*i, y-bots[j], color=color_scn[i], width=width, bottom=bots[j], alpha=alpha)
        if i in [1, 3]:
            if int((y-bots[j])/bots[j]*100) <= 0:
                plt.annotate(str(int((y-bots[j])/bots[j]*100))+'%', xy=(x[j]+width*i+(i-2)*0.1, bots[j]), ha='center')
            else:
                plt.annotate(str(int((y-bots[j])/bots[j]*100))+'%', xy=(x[j]+width*i+(i-2)*0.1, y), ha='center')
        if i == 0:
            bots[j] = y
    # print(i, scn, bots)
plt.legend(frameon=False, loc='upper left')
plt.xticks(x+0.3, labels=Elec_names)
plt.ylim(0, 80)
plt.ylabel('Energy consumption (EJ)', fontsize=12)
plt.text(-0.8, 80*1.01, 'b.', fontsize=25, fontweight='bold')
plt.savefig(r'Figs/Figure_3_a&b.png')
# plt.show()


colors_elec = ['black', 'grey', 'darkred', 'darkviolet', 'royalblue', 'lightskyblue', 'darkorange', 'palegreen']
colors_ene = ['dimgrey', 'brown', 'lightsteelblue', 'slategrey', 'darkblue']
scn = scns[0]
width = 0.3
x1 = np.linspace(1, len(Region)+1, len(Region))
x2 = x1 + width
values = np.zeros(len(Region)*(len(Ene)+len(ElecType)))
names = get_names(RegionSimple, Ene+ElecType)
count = 0
for i, region in enumerate(Region):
    df = pd.read_csv(result_dir + 'res_economy_' + dfs[0] + '.csv')
    total = df[(df['variable']=='output')&(df['year']==2030)&(df['region']==region)&(df['sector'].isin(Ene))]['value'].sum()
    # print(f'region:{region}', f'scenario:{scn}', 'energy', 'total', total)
    bots = 0
    for k, e in enumerate(Ene):
        share = df[(df['variable']=='output')&(df['year']==2030)&(df['region']==region)&(df['sector']==e)]['value'].sum()
        # print(f'region:{region}', f'scenario:{scn}', 'energy', 'share', share)
        if i == 0:
            plt.barh(x1[i], share/total, left=bots, height=width, color=colors_ene[k], label=Ene[k])
        else:
            plt.barh(x1[i], share/total, left=bots, height=width, color=colors_ene[k])
        bots += share / total
        values[count] = share/total
        count += 1
    df = pd.read_csv(result_dir + 'res_energy_' + dfs[0] + '.csv')
    total = df[(df['unit']=='million toe')&(df['year']==2030)&(df['region']==region)&(df['subsector'].isin(ElecType))]['value'].sum()
    # print(f'region:{region}', f'scenario:{scn}', 'electricity', 'total', total)
    bots = 0
    for k, e in enumerate(ElecType):
        share = df[(df['unit']=='million toe')&(df['year']==2030)&(df['region']==region)&(df['subsector']==e)]['value'].sum()
        # print(f'region:{region}', f'scenario:{scn}', 'electricity', 'share', share)
        if i == 0:
            plt.barh(x2[i], share/total, left=bots, height=width, color=colors_elec[k], label=ElecType[k])
        else:
            plt.barh(x2[i], share/total, left=bots, height=width, color=colors_elec[k])
        bots += share / total
        values[count] = share/total
        count += 1
colors_long = (colors_ene+colors_elec)*len(Region)
fig, ax = plt.subplots(figsize=(16, 8), frameon=False)
fig.subplots_adjust(hspace=0.25, wspace=0.45, bottom=0.1, left=0.078, right=0.95, top=0.95)
for j, scn in enumerate(scns[1:]):
    values_scn = np.zeros(len(Region)*(len(Ene)+len(ElecType)))
    count = 0
    for i, region in enumerate(Region):
        df = pd.read_csv(result_dir + 'res_economy_' + dfs[j+1] + '.csv')
        total = df[(df['variable']=='output')&(df['year']==2030)&(df['region']==region)&(df['sector'].isin(Ene))]['value'].sum()
        for k, e in enumerate(Ene):
            share = df[(df['variable']=='output')&(df['year']==2030)&(df['region']==region)&(df['sector']==e)]['value'].sum()
            values_scn[count] = share/total
            count += 1
        df = pd.read_csv(result_dir + 'res_energy_' + dfs[j+1] + '.csv')
        total = df[(df['unit']=='million toe')&(df['year']==2030)&(df['region']==region)&(df['subsector'].isin(ElecType))]['value'].sum()
        for k, e in enumerate(ElecType):
            share = df[(df['unit']=='million toe')&(df['year']==2030)&(df['region']==region)&(df['subsector']==e)]['value'].sum()
            values_scn[count] = share/total
            count += 1
    if j == 0:
        plt.subplot(2, 1, 1)
        plt.yticks([-0.2, -0.1, 0, 0.1, 0.2], labels=['-20%', '-10%', '0', '10%', '20%'])
        plt.ylim(-0.2, 0.2)
        plt.text(0, 0.21, 'SCN1:GwC relative to SCN0')
        plt.text(-2, 0.21, 'c.', fontsize=25, fontweight='bold')
    elif j == 2:
        plt.subplot(2, 1, 2)
        plt.yticks([-0.3, -0.15, 0, 0.15, 0.3], labels=['-30%', '-15%', '0', '15%', '30%'])
        plt.ylim([-0.3, 0.3])
        plt.text(0, 0.315, 'SCN2:GwC relative to SCN0')
        plt.text(-2, 0.315, 'd.', fontsize=25, fontweight='bold')
    else:
        continue
    x = np.linspace(1, 30, 30)
    y, nms, cs = find_top_ten(values_scn - values, names, colors_long)
    plt.bar(x, y, width=0.5, color=cs)
    for k in range(len(nms)):
        if int(y[k]*100) > 0:
            plt.annotate(f'{int(y[k]*100)}%', xy=(x[k], y[k]), ha='center')
        else:
            plt.annotate(f'{int(y[k]*100)}%', xy=(x[k], y[k]-0.03), ha='center')
    plt.hlines(0, xmin=0, xmax=31, color='black', linewidth=0.7)
    plt.xlim(0, 31)
    plt.xticks(x, [item[:item.index('_')] for item in nms], rotation=-45, ha='left', fontsize=10)
    plt.ylabel('Change rate')
plt.savefig(r'Figs/Figure_3_c&d.png')

Sector_new = ['Agriculture & Forestry', 'Fossil fuels', 'Mine & Manufacture', 'Power', 'Services', 'Transportation']
Sec = [
    ["Rice", "Crops nec", "Bovine cattle, sheep and goats, horses", "Animal products nec", "Forestry"],
    ["Coal", "Oil", "Gas", "Petro"],
    ["Mine", "Manufac"],
    ["Power"],
    ["WatWaste", "OthServ"],
    ["Transport"]
]


# Generate figure 3
fig, ax = plt.subplots(figsize=(16, 12), frameon=False)
grid = plt.GridSpec(3, 8, left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
plt.subplot(grid[0, :])
plt.imshow(plt.imread('Figs/Figure_3_a&b.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.subplot(grid[1:3, :])
plt.imshow(plt.imread('Figs/Figure_3_c&d.png'))
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.savefig('Figs/Figure_3.jpg', dpi=600)
