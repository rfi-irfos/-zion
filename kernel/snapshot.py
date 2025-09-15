#!/usr/bin/env python3
# snapshot.py — archive a frozen layer of the repo (ZCP v0.1)

import os, shutil, json, subprocess, pathlib, sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"
LEDGER = ROOT / "ledger" / f"ledger_{datetime.now().year}.jsonl"

SKIP = {"archive", ".git", "__pycache__", ".venv"}

def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def roots_to_copy():
    for p in ROOT.iterdir():
        if p.name in SKIP: 
            continue
        yield p

def snapshot(tag=None):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{ts}_{tag}" if tag else ts
    dest = ARCHIVE / name
    dest.mkdir(parents=True, exist_ok=False)

    for p in roots_to_copy():
        if p.is_dir():
            shutil.copytree(p, dest / p.name)
        else:
            shutil.copy2(p, dest / p.name)

    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT
        ).decode().strip()
    except Exception:
        commit = None

    (dest / "SNAPSHOT.json").write_text(
        json.dumps({"timestamp": now_iso(), "commit": commit, "tag": tag}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(
            {"string": f"snapshot {name}", "number": now_iso(), "symbol": "⬜"},
            ensure_ascii=False
        ) + "\n")

    print(str(dest))

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else None
    snapshot(tag)
