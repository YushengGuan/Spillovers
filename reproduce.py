"""Reproduce the final R2 numerical analyses and figures from frozen inputs."""
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys, time

ROOT = Path(__file__).resolve().parent

def run(script, env):
    print(f'RUN {script}', flush=True)
    subprocess.run([sys.executable, str(ROOT/script)], cwd=ROOT, env=env, check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['all','analysis','figures'], default='all')
    parser.add_argument('--output', type=Path, default=ROOT/'outputs/reproduction')
    args = parser.parse_args()
    out = args.output.resolve()
    # Never allow runtime products to overwrite source data or project code.
    if out == ROOT or any(out == ROOT/p or (ROOT/p) in out.parents for p in ['data','analysis','plotting','cge','scripts','figures','provenance','docs']):
        parser.error('Choose an output directory outside the project source directories.')
    out.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['PYTHONUTF8']='1'
    env['PYTHONIOENCODING']='utf-8'
    started = time.perf_counter()
    if args.stage in ['all','analysis']:
        cost=out/'costs'
        (cost/'QA').mkdir(parents=True, exist_ok=True)
        shutil.copytree(ROOT/'data/figure_source/Costs',cost/'Source_Data',dirs_exist_ok=True)
        shutil.copytree(ROOT/'data/cost_inputs',cost/'Source_Data/Annual_Inputs',dirs_exist_ok=True)
        shutil.copyfile(ROOT/'data/cost_inputs/endpoint_template.csv',cost/'Source_Data/original_mixed_window_results.csv')
        env['SPILLOVERS_WORK']=str(cost)
        for script in ['build_annual.py','complete_all_observed.py','update_endpoints.py']:
            run('analysis/costs/'+script,env)
        env['SPILLOVERS_OUTPUT']=str(out)
        run('analysis/refit_regressions.py',env)
        cge=out/'cge'
        shutil.copytree(ROOT/'data/cge/inputs',cge/'inputs',dirs_exist_ok=True)
        shutil.copytree(ROOT/'cge/src',cge/'src',dirs_exist_ok=True)
        env['SPILLOVERS_CGE_WORK']=str(cge)
        run('analysis/cge/analyze.py',env)
    if args.stage in ['all','figures']:
        work=out/'figures'
        for folder in ['Figures','QA']: (work/folder).mkdir(parents=True, exist_ok=True)
        shutil.copytree(ROOT/'data/figure_source',work/'Source_Data',dirs_exist_ok=True)
        shutil.copytree(ROOT/'data/cge/tables',work/'inputs',dirs_exist_ok=True)
        if args.stage=='all':
            # Plot the freshly recomputed numerical results, not the archived answers.
            for name in ['results.csv','annual_country_costs_completed.csv','annual_plot_costs.csv','observation_imputation_audit.csv']:
                shutil.copyfile(out/'costs/Source_Data'/name,work/'Source_Data/Costs'/name)
            for p in (work/'inputs').glob('*.csv'):
                shutil.copyfile(out/'cge/output/tables'/p.name,p)
        env['SPILLOVERS_WORK']=str(work)
        run('plotting/render_all.py',env)
    env['SPILLOVERS_OUTPUT']=str(out)
    env['SPILLOVERS_STAGE']=args.stage
    run('scripts/validate_results.py',env)
    print(f'COMPLETE in {time.perf_counter()-started:.1f} seconds: {out}',flush=True)

if __name__=='__main__': main()
