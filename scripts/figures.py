#!/usr/bin/env python3
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from counterfactual_release.figures import render
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,default=Path('output/results.json'));p.add_argument('--output',type=Path,default=Path('output/figures'));a=p.parse_args();render(a.results,a.output)
