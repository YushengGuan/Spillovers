"""Render in the submission's original order and shared style environment."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parent
for name in ['figure_costs.py','figures.py','figure_sectors.py']:
    runpy.run_path(str(ROOT/name),run_name='__main__')
