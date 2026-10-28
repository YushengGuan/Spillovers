"""Run the archived CGE model after configuring licensed benchmark inputs."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--preflight',action='store_true')
    p.add_argument('--scenario',choices=['A','B','C','EXPORT','all'],default='all')
    p.add_argument('--julia',default=shutil.which('julia'))
    p.add_argument('--external-model-data',type=Path,help='Directory containing authorized input/ and param/ trees')
    p.add_argument('--runtime',type=Path,default=ROOT/'.cge_runtime')
    a=p.parse_args()
    core=ROOT/'cge/model'
    data=a.external_model_data or core
    inventory=json.loads((ROOT/'cge/required_external_files.json').read_text())
    missing=[x['relative_path'] for x in inventory if not (data/x['relative_path']).is_file()]
    issues=[]
    if not a.julia:issues.append('Julia executable not found; use --julia or add it to PATH.')
    if not os.environ.get('PATH_LICENSE_STRING'):issues.append('PATH_LICENSE_STRING is not set.')
    if missing:issues.append(f'{len(missing)} archived external model input files are missing. See cge/required_external_files.json.')
    mismatched=[x['relative_path'] for x in inventory if (data/x['relative_path']).is_file() and hashlib.sha256((data/x['relative_path']).read_bytes()).hexdigest()!=x['sha256']]
    if mismatched:issues.append(f'{len(mismatched)} external inputs differ from the archived benchmark checksums. Use the matching final-version inputs.')
    if issues:
        print('\n'.join(issues));return 2
    if a.preflight:print('Preflight passed. Numerical solve has not been run.');return 0
    rt=a.runtime.resolve()
    if rt==ROOT or any(rt==ROOT/n or (ROOT/n) in rt.parents for n in ['data','cge','plotting','analysis','scripts']):p.error('Runtime must not overwrite package sources.')
    rt.mkdir(parents=True,exist_ok=True)
    shutil.copytree(core/'jl_r18s15',rt/'model/jl_r18s15',dirs_exist_ok=True)
    for group in ['input','param']:shutil.copytree(data/group,rt/'model'/group,dirs_exist_ok=True)
    shutil.copytree(ROOT/'data/cge/inputs',rt/'inputs',dirs_exist_ok=True)
    shutil.copytree(ROOT/'cge/src',rt/'src',dirs_exist_ok=True)
    env=os.environ.copy();env['JULIA_NUM_THREADS']='1';env['GRID_VERBOSE_INPUTS']='0'
    for scenario in (['A','B','C','EXPORT'] if a.scenario=='all' else [a.scenario]):
        env['LEGACY_RUN_ID']=scenario
        subprocess.run([a.julia,'--startup-file=no',f'--project={ROOT/"cge"}',str(rt/'src/runner.jl'),str(rt),'fiveyear_2050',scenario,'2050'],cwd=rt,env=env,check=True)
    print(f'CGE outputs: {rt/"equilibria_final/fiveyear_2050"}')
    print('Set SPILLOVERS_EQUILIBRIA to that directory before running reproduce.py --stage analysis.')
    return 0
if __name__=='__main__':sys.exit(main())
