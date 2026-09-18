"""Portable entry point. The default workflow uses archived final CGE equilibria."""
from pathlib import Path
import argparse, subprocess, sys, time

ROOT=Path(__file__).resolve().parent
STEPS={
    'regressions':['regressions/analyse.py'],
    'costs':['costs/Code/build_annual.py','costs/Code/complete_all_observed.py',
             'costs/Code/update_endpoints.py','plotting/figure_1.py','costs/Code/check_consistency.py'],
    'comparisons':['model_comparison/refit_trials.py','model_comparison/matched/run_analysis.py',
                  'source_comparison/Code/analyze.py','source_comparison/Code/plot_figures.py'],
    'cge-analysis':['cge/prepare.py','cge/analyze.py','cge/analyze_details.py'],
    'figures':['plotting/figure_1.py','plotting/figures_2_3_4.py','plotting/figure_5.py'],
    'verify':['verify.py'],
}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',choices=['all',*STEPS],default='all')
    args=p.parse_args()
    stages=list(STEPS) if args.stage=='all' else [args.stage]
    done=set();start=time.time()
    for stage in stages:
        for script in STEPS[stage]:
            if script in done:continue
            print('RUN',script,flush=True)
            subprocess.run([sys.executable,'-X','utf8',str(ROOT/script)],cwd=ROOT,check=True)
            done.add(script)
    print(f'Completed {len(done)} scripts in {time.time()-start:.1f} seconds.')
if __name__=='__main__':main()
