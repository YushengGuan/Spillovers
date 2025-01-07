import pandas as pd
import numpy as np
import statsmodels.api as sm


def linear_regression(endog, exog):
    mod = sm.OLS(endog, exog).fit()
    print(mod.summary())
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


df_capacity_solar = pd.read_excel('Dataset.xlsx', sheet_name='Capacity_solar')
df_capacity_wind = pd.read_excel('Dataset.xlsx', sheet_name='Capacity_wind')
df_cost_solar = pd.read_excel('Dataset.xlsx', sheet_name='Cost_solar')
df_cost_wind = pd.read_excel('Dataset.xlsx', sheet_name='Cost_wind')
df_lcoe_solar = pd.read_excel('Dataset.xlsx', sheet_name='LCOE_solar')
df_lcoe_wind = pd.read_excel('Dataset.xlsx', sheet_name='LCOE_wind')

country_wind = ['Global', 'Denmark', 'United States', 'Germany', 'Sweden', 'Italy', 'United Kingdom', 'India',
                'Spain', 'Canada', 'France', 'Turkey', 'Brazil']
country_solar = ['Global', 'Australia', 'France', 'Germany', 'India', 'Italy', 'Japan', 'South Korea', 'Spain',
                 'United Kingdom', 'United States']

reg_result = pd.DataFrame(columns=country_solar)
for c in country_solar:
    if c != 'Japan':  # there is no data of total installed cost in 2010 in Japan
        cost = np.array(df_cost_solar[c])
        capacity_global = np.array(df_capacity_solar['Global_cum'])[0:13]
        price_si = np.array(df_cost_solar['price_si'])
    else:
        cost = np.array(df_cost_solar[c])[1:]
        capacity_global = np.array(df_capacity_solar['Global_cum'])[1:13]
        price_si = np.array(df_cost_solar['price_si'])[1:]
    x = sm.add_constant(np.c_[np.log(capacity_global), np.log(price_si)])
    y = np.log(cost)
    co, se, p = linear_regression(y, x)
    reg_result[c] = [co[0], co[1], co[2], se[0], se[1], se[2], star(p[0]), star(p[1]), star(p[2])]
reg_result.to_excel('Results/Reg_result_solar.xlsx')

reg_result = pd.DataFrame(columns=country_wind)
for c in country_wind:
    cost = np.array(df_cost_wind[c])
    capacity_global = np.array(df_capacity_wind['Global_cum'])[0:13]  # Year 2010-2022
    x = sm.add_constant(np.c_[np.log(capacity_global)])
    y = np.log(cost)
    co, se, p = linear_regression(y, x)
    reg_result[c] = [co[0], co[1], se[0], se[1], star(p[0]), star(p[1])]
reg_result.to_excel('Results/Reg_result_wind.xlsx')

reg_result = pd.DataFrame(columns=country_solar)
for c in country_solar:
    if c != 'Japan':  # there is no data of total installed cost in 2010 in Japan
        cost = np.array(df_cost_solar[c])
        capacity_global = np.array(df_capacity_solar['Global_cum'])[0:13]
        price_si = np.array(df_cost_solar['price_si'])
    else:
        cost = np.array(df_cost_solar[c])[1:]
        capacity_global = np.array(df_capacity_solar['Global_cum'])[1:13]
        price_si = np.array(df_cost_solar['price_si'])[1:]
    x = sm.add_constant(np.c_[np.log(capacity_global), np.log(price_si)])
    y = np.log(cost)
    co, se, p = linear_regression(y, x)
    reg_result[c] = [co[0], co[1], co[2], se[0], se[1], se[2], star(p[0]), star(p[1]), star(p[2])]
reg_result.to_excel('Results/Reg_result_solar.xlsx')

reg_result = pd.DataFrame(columns=country_wind)
for c in country_wind:
    cost = np.array(df_cost_wind[c])
    capacity_global = np.array(df_capacity_wind['Global_cum'])[0:13]  # Year 2010-2022
    x = sm.add_constant(np.c_[np.log(capacity_global)])
    y = np.log(cost)
    co, se, p = linear_regression(y, x)
    reg_result[c] = [co[0], co[1], se[0], se[1], star(p[0]), star(p[1])]
reg_result.to_excel('Results/Reg_result_wind.xlsx')

reg_result = pd.DataFrame(columns=country_solar)
for c in country_solar:
    if c != 'Japan':  # there is no data of LCOE in 2010 in Japan
        cost = np.array(df_lcoe_solar[c])
        capacity_global = np.array(df_capacity_solar['Global_cum'])[0:13]
        price_si = np.array(df_lcoe_solar['price_si'])
    else:
        cost = np.array(df_lcoe_solar[c])[1:]
        capacity_global = np.array(df_capacity_solar['Global_cum'])[1:13]
        price_si = np.array(df_lcoe_solar['price_si'])[1:]
    x = sm.add_constant(np.c_[np.log(capacity_global), np.log(price_si)])
    y = np.log(cost)
    co, se, p = linear_regression(y, x)
    reg_result[c] = [co[0], co[1], co[2], se[0], se[1], se[2], star(p[0]), star(p[1]), star(p[2])]
reg_result.to_excel('Results/Reg_result_solar_lcoe.xlsx')

reg_result = pd.DataFrame(columns=country_wind)
for c in country_wind:
    cost = np.array(df_lcoe_wind[c])
    capacity_global = np.array(df_capacity_wind['Global_cum'])[0:13]  # Year 2010-2022
    x = sm.add_constant(np.c_[np.log(capacity_global)])
    y = np.log(cost)
    co, se, p = linear_regression(y, x)
    reg_result[c] = [co[0], co[1], se[0], se[1], star(p[0]), star(p[1])]
reg_result.to_excel('Results/Reg_result_wind_lcoe.xlsx')
