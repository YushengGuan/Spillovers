from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent;CFG=json.loads((ROOT/'config.json').read_text('utf-8'))
RUN=ROOT/'equilibria_final/fiveyear_2050';OUT=ROOT/'output/tables';OUT.mkdir(parents=True,exist_ok=True)
F=CFG['deflator'];YEARS=CFG['years'];REPORT=CFG['report_years'];MAP=CFG['internal_ids'];RE=['Solar','Wind','Hydro','Biomass']
tests=[]
def check(name,ok,value=''):
    tests.append(dict(check=name,status='PASS' if ok else 'FAIL',value=str(value)))
    (ROOT/'output/validation.json').write_text(json.dumps(tests,indent=2),'utf-8')
    assert ok,(name,value)
def write(df,name):df.to_csv(OUT/(name+'.csv'),index=False,encoding='utf-8-sig')
def read(name):return pd.read_csv(RUN/name)
extra=read('macro_extras.csv');aud=read('input_audit.csv');sector=read('sector.csv');energy=read('energy_balances.csv')
raw={};regions=[];powers=[];diags=[]
for sid,sc in MAP.items():
    comp=read(sid+'/completion.csv');check(sc+' solved to 2050',comp.complete.iloc[0] and comp.last_year.iloc[0]==2050)
    mm=read(sid+'/macro.csv');pp=read(sid+'/power.csv');acc=read(sid+'/accounting.csv');tr=read(sid+'/capital_transitions.csv')
    check(sc+' 18 regions 8 nodes',len(mm)==144 and not mm.duplicated(['year','region']).any() and set(mm.year)==set(YEARS))
    check(sc+' 8 technologies',len(pp)==1152 and not pp.duplicated(['year','region','technology']).any())
    check(sc+' budgets factor markets',acc.max_absolute_gap.max()<1e-5,acc.max_absolute_gap.max())
    check(sc+' external balance',acc.groupby('year').foreign_saving.sum().abs().max()<1e-5)
    check(sc+' aggregate capital recursion',tr.identity_residual.abs().max()<1e-7,tr.identity_residual.abs().max())
    check(sc+' GW is generation equivalent',pp.capacity_status.eq('GENERATION_DIVIDED_BY_FIXED_REFERENCE_CF').all())
    check(sc+' conversion identity',np.allclose(pp.capacity_proxy_GW,pp.generation_TWh/(8.76*pp.reference_CF)))
    zz=aud[aud.scenario.eq(sid)];check(sc+' calibration disabled in scenario equilibrium',zz[['calibrate_gdp','calibrate_power','calibrate_capacity']].eq(0).all().all())
    dd=read(sid+'/solve_diagnostics.csv');diags.append(dd.assign(run_id=sid))
    check(sc+' final MCP residual',float(comp.MCP_residual.iloc[0])<=1e-8,float(comp.MCP_residual.iloc[0]))
    for y in YEARS:
        check(f'{sc} {y} checkpoint',(RUN/sid/f'state_{y}.jls').exists())
        last=dd[dd.year.eq(y)].iloc[-1]
        check(f'{sc} {y} accepted equilibrium',last.status=='Solved' and last.residual<=1e-8,last.residual)
    raw[sid]=mm
    ex=extra[extra.scenario.eq(sid)].drop(columns='scenario');mm=mm.merge(ex,on=['year','region'],validate='one_to_one')
    r=mm[['year','region']].copy();r['scenario']=sc
    for old,new in [('real_GDP','real_GDP'),('real_consumption','real_household_consumption'),('real_investment','real_investment'),('government_income','government_income'),('exports_FOB','exports_FOB'),('imports_CIF','imports_CIF')]:r[new]=mm[old]*F
    r['CO2_Mt']=mm.total_CO2;r['power_CO2_Mt']=mm.power_CO2;r['real_wage']=mm.wage/mm.household_price_index
    b=raw['A'][['year','region','log_utility','log_unit_expenditure']]
    z=mm.merge(b,on=['year','region'],suffixes=('','_base'),validate='one_to_one')
    r['EV']=np.exp(z.log_unit_expenditure_base+z.log_utility_base)*np.expm1(z.log_utility-z.log_utility_base)*F
    r['carbon_price_2024USD_t']=mm.carbon_price_2017USD_t*F;r['additional_carbon_price_2024USD_t']=mm.carbon_increment_2024USD_t
    r['renewable_capacity_GW']=mm.renewable_capacity_proxy_GW;r['total_generation_TWh']=mm.generation_TWh;r['renewable_generation_TWh']=mm.renewable_generation_TWh
    r['renewable_generation_share_pct']=100*r.renewable_generation_TWh/r.total_generation_TWh
    regions.append(r);pp['scenario']=sc;powers.append(pp)
regional=pd.concat(regions,ignore_index=True);power=pd.concat(powers,ignore_index=True)
sector['scenario']=sector.scenario.map(MAP);sector.real_output*=F
energy['scenario']=energy.scenario.map(MAP)
write(regional,'regional_equilibria_all_nodes');write(power,'power_equilibria_all_nodes');write(sector,'sector_equilibria_all_nodes');write(energy,'energy_balances_all_nodes')
check('finite main outcomes',np.isfinite(regional.select_dtypes('number')).all().all())
add=['real_GDP','real_household_consumption','real_investment','government_income','exports_FOB','imports_CIF','CO2_Mt','power_CO2_Mt','EV','renewable_capacity_GW','total_generation_TWh','renewable_generation_TWh']
groups=[]
for group,sub in [('GLOBAL',regional),('ROW_EX_CHINA',regional[regional.region.ne('China')]),('CHINA',regional[regional.region.eq('China')])]:
    z=sub.groupby(['scenario','year'],as_index=False)[add].sum();z['group']=group
    z['renewable_generation_share_pct']=100*z.renewable_generation_TWh/z.total_generation_TWh
    p=sub.assign(w=sub.CO2_Mt*sub.carbon_price_2024USD_t).groupby(['scenario','year']).agg(w=('w','sum'),e=('CO2_Mt','sum'),additional_carbon_price_2024USD_t=('additional_carbon_price_2024USD_t','first'))
    p['emissions_weighted_final_carbon_price_2024USD_t']=p.w/p.e
    z=z.merge(p[['additional_carbon_price_2024USD_t','emissions_weighted_final_carbon_price_2024USD_t']],on=['scenario','year']);groups.append(z)
group=pd.concat(groups,ignore_index=True);write(group,'group_equilibria_all_nodes');write(group[group.year.isin(REPORT)],'group_equilibria_report_nodes')
def contrasts(df,keys,metrics):
    z=df[df.scenario.ne('S0_BASELINE')].merge(df[df.scenario.eq('S0_BASELINE')],on=keys,suffixes=('','_REF'),validate='many_to_one');rows=[]
    for col in metrics:
        r=z[keys+['scenario']].copy();r['outcome']=col;r['baseline']=z[col+'_REF'];r['counterfactual']=z[col];r['deviation']=r.counterfactual-r.baseline
        r['deviation_pct_baseline']=100*r.deviation/r.baseline.where(r.baseline>1e-8)
        if col=='EV':r['deviation_pct_baseline']=np.nan
        rows.append(r)
    out=pd.concat(rows,ignore_index=True);return out[out.year.isin(REPORT)]
write(contrasts(group,['group','year'],add+['renewable_generation_share_pct']),'global_and_group_deviations')
write(contrasts(regional,['region','year'],add+['real_wage','renewable_generation_share_pct']),'regional_deviations')
write(contrasts(power,['region','year','technology'],['generation_TWh','capacity_proxy_GW']),'power_deviations')
write(contrasts(sector,['region','year','sector'],['real_output','labor_demand','capital_demand']),'sector_deviations')
mix=[]
for label,sub in [('GLOBAL',energy),('ROW_EX_CHINA',energy[energy.region.ne('China')]),('CHINA',energy[energy.region.eq('China')])]:
    z=sub.groupby(['scenario','year','fuel'],as_index=False)[['household_Mtoe','nonenergy_industries_Mtoe','energy_industries_Mtoe','power_sector_Mtoe','modeled_final_demand_Mtoe']].sum();z['group']=label
    z['final_energy_share_pct']=100*z.modeled_final_demand_Mtoe/z.groupby(['scenario','year']).modeled_final_demand_Mtoe.transform('sum');mix.append(z)
mix=pd.concat(mix);write(mix,'final_energy_mix');write(contrasts(mix,['group','year','fuel'],['modeled_final_demand_Mtoe','final_energy_share_pct']),'final_energy_deviations')
check('final energy excludes transformation',np.allclose(energy.modeled_final_demand_Mtoe,energy.household_Mtoe+energy.nonenergy_industries_Mtoe))
check('final energy shares',np.allclose(mix.groupby(['group','scenario','year']).final_energy_share_pct.sum(),100))
inp=pd.read_csv(ROOT/'inputs/regional_tfp_paths.csv');hist=pd.read_csv(ROOT/'inputs/country_tfp_history.csv')
for (tech,iso),d in hist.groupby(['technology','iso3']):
    d=d.sort_values('year');alpha=d.alpha.iloc[0]
    for s in ['actual','cf']:
        costs=d['cost_'+s].to_numpy()
        expected=costs[0]/costs
        check(f'annual product {tech} {iso} {s}',np.allclose(expected,d['tfp_raw_'+s]))
        check(f'annual inverse growth {tech} {iso} {s}',np.allclose(d['tfp_raw_'+s].to_numpy()[1:]/d['tfp_raw_'+s].to_numpy()[:-1],costs[:-1]/costs[1:]))
    check(f'common factual 2017 normalization {tech} {iso}',np.isclose(d.loc[d.year.eq(2017),'tfp_actual'].iloc[0],1.))
audit=[]
a=aud[aud.scenario.eq('A')].set_index(['year','region'])
for sid in ['B','C']:
    b=aud[aud.scenario.eq(sid)].set_index(['year','region'])
    for tech in ['pv','wind']:
        z=(b[tech+'_tfp']/a[tech+'_tfp']).rename('executed_multiplier').reset_index();z['technology']=tech
        z=z.merge(inp,on=['year','region','technology']);z['scenario']=MAP[sid];audit.append(z)
        check(f'{sid} {tech} executed compound multiplier',np.allclose(z.executed_multiplier,z.tfp_multiplier,rtol=1e-10))
    check(sid+' same macro productivity',np.allclose(a.macro_tfp,b.macro_tfp))
write(pd.concat(audit),'tfp_mapping_audit')
write(inp,'regional_tfp_paths');write(hist,'country_tfp_history');write(pd.concat(diags),'all_solve_attempts')
pol=read('capacity_policy_selected.csv');write(pol,'capacity_policy_selected');write(read('capacity_price_search.csv'),'capacity_price_search')
check('baseline target',abs(group.query('group=="GLOBAL" and scenario=="S0_BASELINE" and year==2030').renewable_capacity_GW.iloc[0]-11000)<.01)
check('policy target',abs(group.query('group=="GLOBAL" and scenario=="S2_CAPACITY" and year==2030').renewable_capacity_GW.iloc[0]-11000)<.1)
check('policy price persistent',regional[regional.scenario.eq('S2_CAPACITY')].additional_carbon_price_2024USD_t.nunique()==1)
runner=(ROOT/'src/runner.jl').read_text('utf-8')
check('no installed stock or generation ceiling module',all(s not in runner for s in ['renewable_capital.jl','equipment_satellite.jl']))
check('no direct investment efficiency shock','knowledge_investment_efficiency' not in (ROOT/'src/experiment.jl').read_text('utf-8'))
for rec in CFG['sources']:check('cost input unchanged '+Path(rec['source']).parts[-3],hashlib.sha256((ROOT.parent/rec['source']).read_bytes()).hexdigest()==rec['sha256'])
key=group.query('group=="GLOBAL" and year in [2030,2050]');write(key,'global_2030_2050')
summary={}
for _,z in key.iterrows():
    b=key[(key.scenario=='S0_BASELINE')&(key.year==z.year)].iloc[0];d=z.to_dict()
    for col in ['real_GDP','CO2_Mt','renewable_capacity_GW','renewable_generation_TWh','renewable_generation_share_pct']:
        d[col+'_gap']=float(z[col]-b[col]);d[col+'_pct_gap']=float(100*(z[col]-b[col])/b[col])
    summary[f'{z.scenario}_{z.year}']=d
(ROOT/'output/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8')
write(pd.DataFrame(tests),'validation_checks')
print(key[['scenario','year','renewable_capacity_GW','CO2_Mt','real_GDP','EV','additional_carbon_price_2024USD_t']].to_string(index=False));print('PASS',len(tests))
