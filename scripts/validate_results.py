"""Compare recomputed values with the frozen final manuscript data."""
from pathlib import Path
import json, os
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ['SPILLOVERS_OUTPUT'])
stage=os.environ['SPILLOVERS_STAGE']
checks=[]
def compare(actual,expected,keys):
    a=pd.read_csv(actual).sort_values(keys).reset_index(drop=True)
    b=pd.read_csv(expected).sort_values(keys).reset_index(drop=True)
    assert len(a)==len(b),(actual,len(a),len(b))
    assert a[keys].equals(b[keys]),(actual,'keys differ')
    columns=[c for c in b.select_dtypes(include='number') if c in a]
    for c in columns:
        assert np.allclose(a[c],b[c],rtol=1e-9,atol=1e-7,equal_nan=True),(actual,c)
    checks.append(dict(file=str(actual.relative_to(OUT)),rows=len(a),numeric_columns=len(columns),status='PASS'))
if stage in ['all','analysis']:
    for n,keys in [('results.csv',['technology','iso3']),('annual_country_costs_completed.csv',['technology','iso3','year']),('annual_plot_costs.csv',['technology','year']),('observation_imputation_audit.csv',['technology','iso3','year'])]:
        compare(OUT/'costs/Source_Data'/n,ROOT/'data/figure_source/Costs'/n,keys)
    keys_by_file={
      'group_equilibria_all_nodes.csv':['scenario','year','group'],
      'regional_equilibria_all_nodes.csv':['scenario','year','region'],
      'power_equilibria_all_nodes.csv':['scenario','year','region','technology'],
      'sector_equilibria_all_nodes.csv':['scenario','year','region','sector'],
      'final_energy_mix.csv':['scenario','year','group','fuel'],
      'capacity_price_search.csv':['additional_price_2024USD_t'],
      'capacity_policy_selected.csv':['additional_price_2024USD_t']}
    for n,keys in keys_by_file.items():compare(OUT/'cge/output/tables'/n,ROOT/'data/cge/tables'/n,keys)
if stage in ['all','figures']:
    for name,keys in [('weighted_shapley_summary.csv',['technology','sample']),('annual_plot_costs.csv',['technology','year'])]:
        compare(OUT/'figures/Source_Data/Costs'/name,ROOT/'data/figure_source/Costs'/name,keys)
    import xml.etree.ElementTree as ET
    files=sorted((OUT/'figures/Figures').glob('*.svg'))
    assert len(files)==5,len(files)
    for f in files:
        e=ET.parse(f).getroot()
        assert len(e.findall('.//{http://www.w3.org/2000/svg}image'))==0,f
        assert abs(float(e.attrib['width'].replace('pt',''))*25.4/72-183)<.01,f
        checks.append(dict(file=str(f.relative_to(OUT)),status='PASS',width_mm=183,embedded_bitmap_count=0))
(OUT/'validation.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(checks)} numerical and vector-format comparisons.')
