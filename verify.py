"""Verify final numerical identities; optionally check the untouched release hashes."""
from pathlib import Path
import argparse, csv, hashlib, json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
def read(rel):return pd.read_csv(ROOT/rel)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity',action='store_true',help='Check original release hashes before regeneration.')
    args=parser.parse_args()
    if args.integrity:
        with (ROOT/'MANIFEST_SHA256.csv').open(encoding='utf8',newline='') as f:
            for row in csv.DictReader(f):
                path=ROOT/row['file']
                check('file exists: '+row['file'],path.is_file())
                check('SHA256: '+row['file'],hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'])

    a=read('costs/Source_Data/annual_country_costs_completed.csv')
    effects=['P_direct','S_share','T_cn_tariff','K_spillover','G_other']
    check('345 unique country-years',len(a)==345 and not a.duplicated(['technology','iso3','year']).any())
    check('10 PV and 13 wind countries',a.groupby('technology').iso3.nunique().to_dict()=={'pv':10,'wind':13})
    check('334 observed cells',int(a.observed.notna().sum())==334)
    check('15 years per country',a.groupby(['technology','iso3']).year.nunique().eq(15).all())
    check('positive fitted factual/counterfactual costs',(a[['model_factual','model_without_china_contribution']]>0).all().all())
    check('mechanism sum',np.allclose(a[effects].sum(axis=1),a.china_contribution_since_2010))
    check('counterfactual cost identity',np.allclose(a.model_without_china_contribution-a.model_factual,a.china_contribution_since_2010))
    check('zero contribution in 2010',np.allclose(a.loc[a.year.eq(2010),'china_contribution_since_2010'],0))
    check('zero wind E',np.allclose(a.loc[a.technology.eq('wind'),'G_other'],0))
    for tech,value in [('pv',1313.3084738284274),('wind',378.5992545497498)]:
        z=a[a.technology.eq(tech)&a.year.eq(2024)]
        check(tech+' final weighted net contribution',abs(float(z.weight@z.china_contribution_since_2010)-value)<1e-6)
    ref=read('reference/costs/annual_country_costs_completed.csv')
    keys=['technology','iso3','year'];cols=effects+['model_factual','model_without_china_contribution']
    check('final cost reference reproduced',np.allclose(a.set_index(keys).sort_index()[cols],ref.set_index(keys).sort_index()[cols]))

    rc=read('regressions/results/archive_reproduction_checks.csv')
    check('selected regression coefficients reproduced',rc.coef_abs_error.max()<1e-8)
    check('selected HAC errors reproduced',rc.se_abs_error.max()<1e-7)
    coeff=read('regressions/results/coefficient_comparison.csv')
    check('34 selected equations',coeff.id.nunique()==34)
    alt=read('model_comparison/results/refit_checks.csv')
    check('supplemental coefficients reproduced',alt.coefficient_error.max()<1e-7)
    check('supplemental HAC errors reproduced',alt.SE_error.max()<1e-6)
    matched=json.loads((ROOT/'model_comparison/matched/audit.json').read_text('utf8'))
    check('matched model comparison passes',matched['passed'])

    v=read('cge/output/tables/validation_checks.csv')
    check('CGE postprocessing checks pass',v.status.eq('PASS').all())
    g=read('cge/output/tables/group_equilibria_all_nodes.csv').query('group=="GLOBAL"').set_index(['scenario','year'])
    check('S0 2030 target',abs(g.loc[('S0_BASELINE',2030),'renewable_capacity_GW']-11000)<.01)
    check('S2 2030 target',abs(g.loc[('S2_CAPACITY',2030),'renewable_capacity_GW']-11000)<.1)
    expected={('S1_NO_CN',2030):(9046.51,152.08,-128.97,-249.28),
              ('S2_CAPACITY',2030):(10999.96,-7815.43,-761.48,-2047.73),
              ('S1_NO_CN',2050):(12429.26,188.91,-106.78,-379.45),
              ('S2_CAPACITY',2050):(15464.15,-9170.81,-1461.92,-2832.05)}
    for (sc,year),values in expected.items():
        z=g.loc[(sc,year)];b=g.loc[('S0_BASELINE',year)]
        actual=[z.renewable_capacity_GW,z.CO2_Mt-b.CO2_Mt,z.real_GDP-b.real_GDP,z.EV]
        check(f'{sc} {year} manuscript outcomes',np.allclose(actual,values,atol=.011,rtol=0))
    policy=read('cge/output/tables/capacity_policy_selected.csv')
    check('carbon-price increment',abs(policy.additional_price_2024USD_t.iloc[0]-60.893893166004126)<1e-8)
    hist=read('cge/inputs/country_tfp_history.csv').query('iso3!="CHN"')
    check('country inverse-cost productivity ratio',np.allclose(hist.tfp_multiplier,hist.cost_actual/hist.cost_cf))

    common=read('source_comparison/Source_Data/weighted_endpoints.csv').query('scope=="common_receivers"')
    check('source comparison common samples',common.groupby('technology').n.first().to_dict()=={'pv':8,'wind':11})
    check('historical source component sums',np.allclose(common[['P','S','T','K','E']].sum(axis=1),common.net))
    joint=read('source_comparison/Source_Data/joint_2024_summary.csv').query('target=="JOINT"').set_index('technology')
    check('joint PV diagnostic',abs(joint.loc['pv','total_gap']-560.5)<.05)
    check('joint wind diagnostic',abs(joint.loc['wind','total_gap']-184.8)<.05)
    for stem in ['Figure1_costs','Figure2_transition','Figure3_emissions','Figure4_equity','Figure5_sectoral_output']:
        for ext in ['pdf','svg','png','tiff']:
            p=ROOT/'Figures'/f'{stem}.{ext}'
            check(f'figure {stem}.{ext}',p.is_file() and p.stat().st_size>1000)
    result={'all_pass':True,'checks':checks,'full_CGE_resolved_by_this_check':False}
    # A deterministic record: file integrity checks are not stored because the
    # record itself belongs to the release manifest.
    result['checks']=[c for c in checks if not c['check'].startswith(('SHA256:','file exists:'))]
    (ROOT/'QA').mkdir(exist_ok=True)
    (ROOT/'QA/release_verification.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(f'PASS: {len(checks)} checks; all final numerical references reproduced.')

if __name__=='__main__':main()
