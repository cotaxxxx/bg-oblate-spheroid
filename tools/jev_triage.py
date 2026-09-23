#!/usr/bin/env python3
"""Non-binding Jev triage gate for research audit receipts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run a non-binding Jev yes/no triage over a text file."
    )
    ap.add_argument("file", type=Path)
    ap.add_argument("question")
    ap.add_argument("--true", dest="true_desc", default="The assertion is supported")
    ap.add_argument("--false", dest="false_desc", default="The assertion is not supported")
    ap.add_argument("--threshold", type=float, default=0.90)
    ap.add_argument("--model", default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if not 0.5 <= args.threshold <= 1.0:
        ap.error("--threshold must be in [0.5, 1.0]")
    data = args.file.read_bytes()

    cmd = [
        "jev", "yes", args.question,
        "-s", f"@{args.file}",
        "--json",
        "--true", args.true_desc,
        "--false", args.false_desc,
    ]
    if args.model:
        cmd += ["--model", args.model]

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120, check=False
        )
    except Exception as exc:
        record = {
            "status": "JEV_TRIAGE_ERROR",
            "error": f"{type(exc).__name__}: {exc}",
            "binding": False,
        }
        print(json.dumps(record, ensure_ascii=False))
        return 3

    try:
        raw = json.loads(proc.stdout)
        answer = raw["answer"]
        probability = float(answer["noul"])
        yes = bool(answer["yes"])
        if proc.returncode not in (0, 1):
            raise RuntimeError(f"unexpected Jev exit code {proc.returncode}")
    except Exception as exc:
        record = {
            "status": "JEV_TRIAGE_ERROR",
            "error": f"unexpected Jev JSON: {type(exc).__name__}: {exc}",
            "binding": False,
        }
        print(json.dumps(record, ensure_ascii=False))
        return 3

    ok = yes and probability >= args.threshold
    record = {
        "status": "JEV_TRIAGE_OK" if ok else "JEV_TRIAGE_REVIEW",
        "binding": False,
        "certification": "NOT_CERTIFICATION",
        "input_file": str(args.file),
        "input_sha256": sha256_bytes(data),
        "question": args.question,
        "threshold": args.threshold,
        "answer_yes": yes,
        "probability": probability,
        "provider": raw.get("provider"),
        "model": raw.get("model"),
        "usage": raw.get("usage"),
    }
    rendered = json.dumps(record, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
