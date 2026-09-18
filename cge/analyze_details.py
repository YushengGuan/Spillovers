from pathlib import Path
import pandas as pd,numpy as np,json,shutil
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent
RT=ROOT/'equilibria_final/fiveyear_2050'
T=ROOT/'output/tables';OUT=REPO;D=T
MAP={'A':'S0_BASELINE','B':'S1_NO_CN','C':'S2_CAPACITY'}
def contrast(df,keys,metrics):
    base=df[df.scenario.eq('S0_BASELINE')].drop(columns='scenario')
    z=df[df.scenario.ne('S0_BASELINE')].merge(base,on=keys,suffixes=('','_S0'),validate='many_to_one')
    for k in metrics:
        z[k+'_gap']=z[k]-z[k+'_S0'];z[k+'_pct']=100*z[k+'_gap']/z[k+'_S0'].where(abs(z[k+'_S0'])>1e-10)
    return z
for name,keys,metrics in [
 ('sector_emissions',['year','region','sector'],['CO2_Mt']),
 ('power_emissions',['year','region','technology'],['CO2_Mt']),
 ('household_consumption',['year','region','good'],['quantity','consumer_price','expenditure_2024USD_bn','real_consumption_2024USD_bn']),
 ('household_incomes',['year','region'],['household_income','labor_income','household_capital_income','land_income','resource_income','government_income','carbon_revenue'])]:
    df=pd.read_csv(RT/(name+'.csv'));df.scenario=df.scenario.map(MAP)
    df.to_csv(T/(name+'.csv'),index=False)
    z=contrast(df,keys,metrics);z.to_csv(T/(name+'_contrasts.csv'),index=False)
sec=pd.read_csv(T/'sector_emissions_contrasts.csv')
power=pd.read_csv(T/'power_emissions_contrasts.csv')
hh=pd.read_csv(T/'household_consumption_contrasts.csv')
inc=pd.read_csv(T/'household_incomes_contrasts.csv')
regional=pd.read_csv(T/'regional_equilibria_all_nodes.csv')
rr=contrast(regional,['year','region'],['real_GDP','CO2_Mt','power_CO2_Mt','real_household_consumption'])
rr['EV_pct_C0']=100*rr.EV/rr.real_household_consumption_S0
rr.to_csv(T/'regional_narrative_diagnostics.csv',index=False)
g=pd.read_csv(T/'group_equilibria_all_nodes.csv').query('group=="GLOBAL"')
gg=contrast(g,['year','group'],['real_GDP','CO2_Mt','power_CO2_Mt','renewable_capacity_GW'])
pw=pd.read_csv(T/'power_equilibria_all_nodes.csv').groupby(['scenario','year','technology'],as_index=False).generation_TWh.sum()
pg=contrast(pw,['year','technology'],['generation_TWh']);pg.to_csv(T/'global_generation_diagnostics.csv',index=False)
energy=pd.read_csv(T/'final_energy_mix.csv').query('group=="GLOBAL"')
eg=contrast(energy,['year','fuel'],['modeled_final_demand_Mtoe'])
eg.to_csv(T/'global_final_energy_diagnostics.csv',index=False)
et=energy.groupby(['year','scenario'],as_index=False).modeled_final_demand_Mtoe.sum()
ett=contrast(et,['year'],['modeled_final_demand_Mtoe'])
sector=pd.read_csv(T/'sector_equilibria_all_nodes.csv')
ss=contrast(sector,['year','region','sector'],['real_output'])
ss.to_csv(T/'regional_sector_output_diagnostics.csv',index=False)
global_sector=sector.groupby(['year','scenario','sector'],as_index=False).real_output.sum()
gs=contrast(global_sector,['year','sector'],['real_output']);gs.to_csv(T/'global_sector_output_diagnostics.csv',index=False)
recon=pd.read_csv(RT/'emissions_checks.csv')
assert recon.identity_gap.abs().max()<1e-6
rows=[]
for y in [2030,2050]:
    a=pg.query('scenario=="S1_NO_CN" and year==@y').set_index('technology').generation_TWh_gap
    loss=-a[['Solar','Wind']].sum();foss=a[['Coal_Power','Gas_Power','Oil_Power']].sum();other=a[['Hydro','Biomass','Nuclear']].sum()
    rows.append(dict(year=y,pv_wind_loss_TWh=loss,fossil_offset_TWh=foss,other_lowcarbon_offset_TWh=other,total_generation_loss_TWh=-a.sum(),fossil_offset_pct=foss/loss*100,other_offset_pct=other/loss*100,demand_offset_pct=-a.sum()/loss*100))
pd.DataFrame(rows).to_csv(T/'S1_generation_offset.csv',index=False)
shutil.copy2(ROOT/'output/summary.json',D/'summary.json')
print('GLOBAL',gg[['scenario','year','real_GDP_gap','CO2_Mt_gap','power_CO2_Mt_gap','renewable_capacity_GW','EV']].query('year in [2030,2050]').round(4).to_string(index=False))
print('GENERATION',pg.query('year in [2030,2050]')[['scenario','year','technology','generation_TWh_gap']].round(4).to_string(index=False))
print('ENERGY',eg.query('year==2030')[['scenario','fuel','modeled_final_demand_Mtoe_pct']].round(4).to_string(index=False))
print('TOTAL ENERGY',ett.query('year==2030')[['scenario','modeled_final_demand_Mtoe_pct']].round(4).to_string(index=False))
print('OFFSETS',pd.DataFrame(rows).round(4).to_string(index=False))
for s in ['S1_NO_CN','S2_CAPACITY']:
 z=rr.query('scenario==@s and year==2050')
 print('REGIONS',s,z[['region','CO2_Mt_gap','CO2_Mt_pct','power_CO2_Mt_gap','real_GDP_pct','EV_pct_C0']].round(4).to_string(index=False))
 print('GLOBAL SECTORS',s,gs.query('scenario==@s and year==2050')[['sector','real_output_pct']].round(4).to_string(index=False))
print('DETAILS_READY')
