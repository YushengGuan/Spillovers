import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


data_solar = pd.read_excel('Dataset.xlsx', sheet_name='2030_solar')
qt0_solar = data_solar['qt0'].values
qt1_solar = data_solar['qt1'].values
qt2_solar = data_solar['qt2'].values
price_si = data_solar['price_si'].values
data_wind = pd.read_excel('Dataset.xlsx', sheet_name='2030_wind')
qt0_wind = data_wind['qt0'].values
qt1_wind = data_wind['qt1'].values
qt2_wind = data_wind['qt2'].values

country_wind = ['Global', 'Denmark', 'United States', 'Germany', 'Sweden', 'Italy', 'United Kingdom', 'India', 'Spain', 'Canada', 'France', 'Turkey', 'Brazil']
country_solar = ['Global', 'Australia', 'France', 'Germany', 'India', 'Italy', 'Japan', 'South Korea', 'Spain', 'United Kingdom', 'United States']
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

# total installed cost of solar PV
df_co = pd.read_excel(f'Results\\Reg_result_solar.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
base = 7  # 2017
df_tfp0 = pd.DataFrame(columns=country_solar, index=range(2017, 2031))
df_tfp1 = pd.DataFrame(columns=country_solar, index=range(2017, 2031))
df_tfp2 = pd.DataFrame(columns=country_solar, index=range(2017, 2031))
for i, c in enumerate(country_solar):
    co_effs = df_co[c].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_solar) + co_effs[2]*np.log(price_si))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_solar) + co_effs[2]*np.log(price_si))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_solar) + co_effs[2]*np.log(price_si))
    tfp_0 = 1 / (y_0 / y_0[base])
    tfp_1 = 1 / (y_1 / y_0[base])
    tfp_2 = 1 / (y_2 / y_0[base])
    df_tfp0[c] = tfp_0[7:]
    df_tfp1[c] = tfp_1[7:]
    df_tfp2[c] = tfp_2[7:]
df_tfp0.to_csv('Results/TFP0_solar.csv')
df_tfp1.to_csv('Results/TFP1_solar.csv')
df_tfp2.to_csv('Results/TFP2_solar.csv')

# total installed cost of wind power
df_co = pd.read_excel(f'Results\\Reg_result_wind.xlsx')
df = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
base = 7  # 2017
df_tfp0 = pd.DataFrame(columns=country_wind, index=range(2017, 2031))
df_tfp1 = pd.DataFrame(columns=country_wind, index=range(2017, 2031))
df_tfp2 = pd.DataFrame(columns=country_wind, index=range(2017, 2031))
for i, c in enumerate(country_wind):
    co_effs = df_co[c].values
    y_0 = np.exp(co_effs[0] + co_effs[1]*np.log(qt0_wind))
    y_1 = np.exp(co_effs[0] + co_effs[1]*np.log(qt1_wind))
    y_2 = np.exp(co_effs[0] + co_effs[1]*np.log(qt2_wind))
    tfp_0 = 1 / (y_0 / y_0[base])
    tfp_1 = 1 / (y_1 / y_0[base])
    tfp_2 = 1 / (y_2 / y_0[base])
    df_tfp0[c] = tfp_0[7:]
    df_tfp1[c] = tfp_1[7:]
    df_tfp2[c] = tfp_2[7:]
df_tfp0.to_csv('Results/TFP0_wind.csv')
df_tfp1.to_csv('Results/TFP1_wind.csv')
df_tfp2.to_csv('Results/TFP2_wind.csv')


path = r'Results/{}.csv'
path2 = 'E:\Online files\关钰生\我的资料库\私人资料库\科研\GRID-Core\input\elec\{}.csv'
# CGE model input
def transform_solar(df, scn, path=path2):
    result = pd.DataFrame(columns=Region, index=range(2017, 2031))
    df_cn = pd.read_csv('Results/TFPs_China.csv')
    for region in Region:
        if region == 'Australia_Oceania':
            result[region] = df['Australia'].values
        elif region == 'China':
            result[region] = df_cn['Solar'].values
        elif region == 'South Korea':
            result[region] = df['South Korea'].values
        elif region == 'Japan':
            result[region] = df['Japan'].values
        elif region == 'India':
            result[region] = df['India'].values
        elif region == 'United States':
            result[region] = df['United States'].values
        elif region == 'EU, UK and EFTA':
            value = np.zeros(14)
            for country in ['France', 'Germany', 'Italy', 'Spain', 'United Kingdom']:
                value += df[country].values
            result[region] = value / 5
        else:
            result[region] = df['Global'].values
    result.to_csv(path.format(scn))
    print(result)
    return f'{scn} transformation complete!'

transform_solar(pd.read_csv(r'Results/TFP0_solar.csv'), 'tfp0_solar')
transform_solar(pd.read_csv(r'Results/TFP1_solar.csv'), 'tfp1_solar')
transform_solar(pd.read_csv(r'Results/TFP2_solar.csv'), 'tfp2_solar')


def transform_wind(df, scn, path=path2):
    result = pd.DataFrame(columns=Region, index=range(2017, 2031))
    df_cn = pd.read_csv('Results/TFPs_China.csv')
    for region in Region:
        if region == 'Canada':
            result[region] = df['Canada'].values
        elif region == 'China':
            result[region] = df_cn['Wind'].values
        elif region == 'Brazil':
            result[region] = df['Brazil'].values
        elif region == 'Central, Western and South Asia':
            result[region] = df['Turkey'].values
        elif region == 'India':
            result[region] = df['India'].values
        elif region == 'United States':
            result[region] = df['United States'].values
        elif region == 'EU, UK and EFTA':
            value = np.zeros(14)
            for country in ['France', 'Germany', 'Italy', 'Spain', 'United Kingdom', 'Denmark', 'Sweden']:
                value += df[country].values
            result[region] = value / 7
        else:
            result[region] = df['Global'].values
    result.to_csv(path.format(scn))
    print(result)
    return f'{scn} transformation complete!'


transform_wind(pd.read_csv(r'Results/TFP0_wind.csv'), 'tfp0_wind')
transform_wind(pd.read_csv(r'Results/TFP1_wind.csv'), 'tfp1_wind')
transform_wind(pd.read_csv(r'Results/TFP2_wind.csv'), 'tfp2_wind')
