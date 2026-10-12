#!/home/daybreak/.pyenv/versions/3.11.16/bin/python
"""Kernel-free D-OB P2 V3 checker initial-id controls (d)-(f)."""
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

C = load("d_ob_p2_checker_v3_controls", "checker/d_ob_p2_checker.py")
active = C.active_indices()
records = [{"initial": list(x)} for x in active]
C.validate_initial_ids(records)
print(f"CHECKER_CONTROL_D PASS active_ids={len(active)}")
for label, bad in (
    ("E", records[:-1]),
    ("F", records + [{"initial": [7,7,0]}]),
):
    try:
        C.validate_initial_ids(bad)
    except ValueError as exc:
        print(f"CHECKER_CONTROL_{label} PASS rejected={type(exc).__name__}:{exc}")
    else:
        raise AssertionError(f"checker control {label} unexpectedly accepted")
print("CHECKER_CONTROLS_PASS D E F KERNEL_NOT_EVALUATED")
