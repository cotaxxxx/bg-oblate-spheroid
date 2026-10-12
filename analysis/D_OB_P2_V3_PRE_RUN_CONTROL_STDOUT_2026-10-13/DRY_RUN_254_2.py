#!/home/daybreak/.pyenv/versions/3.11.16/bin/python
"""Kernel-free D-OB P2 V3 active-initial enumeration control."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

P = load("d_ob_p2_producer_v3_dry", "producer/d_ob_p2_producer.py")
active = P.all_indices()
full = [(i,j,k) for i in range(8) for j in range(8) for k in range(4)]
excluded = [x for x in full if x not in set(active)]
assert len(active) == 254
assert excluded == [(0,0,3),(7,7,0)]
assert active == [x for x in full if x not in {(0,0,3),(7,7,0)}]
print(f"DRY_RUN_ACTIVE_COUNT PASS count={len(active)}")
print("DRY_RUN_EXCLUDED PASS ids=" + ",".join(map(str, excluded)))
print(f"DRY_RUN_CANONICAL_ORDER PASS equal={active == [x for x in full if x not in set(excluded)]}")
print(f"DRY_RUN_FIRST_LAST PASS first={active[0]} last={active[-1]}")
print("DRY_RUN_PASS 254_ACTIVE 2_EXCLUDED CANONICAL_ORDER")
