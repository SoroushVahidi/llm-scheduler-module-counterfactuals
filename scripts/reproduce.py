#!/usr/bin/env python3
"""Run all supported Level-1 calculations; never runs a simulation."""
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from counterfactual_release.analysis import run
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));a=p.parse_args()
r=run(a.output);print(r['verification'])
