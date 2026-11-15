"""Runtime provenance pins for C gap 2; does NOT touch sealed ledgers."""
from __future__ import annotations

import hashlib
import importlib.metadata
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENT = "26d81e1049340d44ef7f08ae8e17d0692983395b"
BASE_NEW = "3bd5113e7d26e2860ddb8228904d977842aef541"
PREVIOUS_NEW = "ff07e097c098ace4051b04b76d410713fb59490a"
PREVIOUS_PREVIOUS_NEW = "45617d0ad8aa5c61cf858556791b38794929f9a7"

EXPECTED_CHANGED = frozenset({
    "gap1_producer/global_axial_c1b_kernel.py",
    "gap1_checker/global_axial_c1b_kernel.py",
    "gap1_producer/global_axial_c1b_gating.py",
    "gap1_checker/global_axial_c1b_gating.py",
    "gap2_analysis/README_C_GAP2_V4_R2.md",
    "gap2_analysis/__init__.py",
    "gap2_analysis/endpoint_driver.py",
    "gap2_analysis/run4_regression.py",
    "gap2_analysis/sealed_contract.py",
    "gap2_checker/__init__.py",
    "gap2_checker/driver.py",
    "gap2_producer/__init__.py",
    "gap2_producer/driver.py",
})

RUN4_SEVEN = {
    "gap1_analysis/c1b_resumable_driver.py",
    "gap1_producer/global_axial_c1b_gating.py",
    "gap1_checker/global_axial_c1b_gating.py",
    "gap1_producer/global_axial_c1b_kernel.py",
    "gap1_checker/global_axial_c1b_kernel.py",
    "gap1_producer/global_axial_c1b_producer.py",
    "gap1_checker/global_axial_c1b_checker.py",
}


def git(*args):
    proc = subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, check=True)
    return proc.stdout.strip()


def files_sha256(path):
    with path.open("rb") as h:
        return hashlib.file_digest(h, "sha256").hexdigest()


def runtime_identity(kernel):
    """Snapshot before & after. Rejected unless working tree AND imports are pinned."""
    head = git("rev-parse", "HEAD")
    expected_parent = git("rev-parse", "HEAD^")
    if expected_parent != BASE_NEW:
        raise RuntimeError("GAP2_IMPLEMENTATION_PARENT_MISMATCH")
    previous_parent = git("rev-parse", BASE_NEW + "^")
    previous_previous_parent = git("rev-parse", BASE_NEW + "^^")
    original_parent = git("rev-parse", BASE_NEW + "^^^")
    if (previous_parent != PREVIOUS_NEW
            or previous_previous_parent != PREVIOUS_PREVIOUS_NEW
            or original_parent != PARENT):
        raise RuntimeError("RUN4_PARENT_MISMATCH")
    if git("status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError("RUNTIME_WORKTREE_NOT_CLEAN")
    changed = set(git("diff", "--name-only", PARENT, "HEAD").splitlines())
    if not EXPECTED_CHANGED.issubset(changed):
        raise RuntimeError("RUNTIME_ORIGINAL_13_FILES_MISSING")
    run4 = set(RUN4_SEVEN) | set(kernel.GAP1_IMPORT_CLOSURE_17) | set(kernel.GAP1_READ_ONLY_PINS)
    if len(run4) != 25:
        raise RuntimeError("RUN4_IMPORT_CLOSURE_COUNT_MISMATCH")
    if not (set(kernel.GAP1_IMPORT_CLOSURE_17) | set(kernel.GAP1_READ_ONLY_PINS)).issubset(
            changed | set(git("ls-tree", "-r", "--name-only", "HEAD").splitlines())):
        raise RuntimeError("IMPORT_CLOSURE_FILE_MISSING")
    # G3: pinned files are the SAME across both lineages. Do not pollute
    # this dictionary with role-dependent sys.modules imports.
    blobs = {}
    for rel in sorted(changed | run4):
        path = ROOT / rel
        if not path.is_file():
            raise RuntimeError("PINNED_SOURCE_FILE_MISSING:" + rel)
        expected = git("rev-parse", "HEAD:" + rel)
        observed = git("hash-object", "--", str(path))
        if expected != observed:
            raise RuntimeError("PINNED_FILE_BLOB_CHANGED:" + rel)
        blobs[rel] = {"blob": observed, "sha256": files_sha256(path)}
    run4_blobs = {name: git("rev-parse", PARENT + ":" + name) for name in sorted(run4)}
    imported = {}
    root = ROOT.resolve()
    for name, module in sorted(sys.modules.copy().items()):
        raw = getattr(module, "__file__", None)
        if not raw:
            continue
        path = Path(raw).resolve()
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if path.suffix != ".py":
            continue
        relative_name = relative.as_posix()
        if relative_name not in blobs:
            # Audit additional imported repo files, but keep them in the
            # ROLE-DEPENDENT import_closure dictionary alone.
            if not path.is_file():
                raise RuntimeError("IMPORT_FILE_MISSING")
            expected = git("rev-parse", "HEAD:" + relative_name)
            actual = git("hash-object", "--", str(path))
            if expected != actual:
                raise RuntimeError("IMPORT_BLOB_MISMATCH")
            entry = {"blob": actual, "sha256": files_sha256(path)}
        else:
            entry = blobs[relative_name]
        imported[name] = {"path": relative_name, **entry}
    return {
        "head": head,
        "direct_parent": expected_parent,
        "frozen_grandparent": original_parent,
        "clean_status": True,
        "changed_13_plus_new": sorted(changed),
        "current_blobs_and_sha256": blobs,
        "run4_frozen_25_blobs": run4_blobs,
        "import_closure": imported,
        "python": sys.version,
        "python_executable": sys.executable,
        "flint_version": importlib.metadata.version("python-flint"),
        "mpmath_version": importlib.metadata.version("mpmath"),
        "platform": platform.platform(),
    }


def verify_end_identity(before, kernel):
    after = runtime_identity(kernel)
    if after != before:
        raise RuntimeError("RUNTIME_POST_IDENTITY_MISMATCH")
    return after
