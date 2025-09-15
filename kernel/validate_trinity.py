#!/usr/bin/env python3
# validate_trinity.py — minimal ledger sanity check (ZCP v0.1)
# Usage: python3 kernel/validate_trinity.py ledger/ledger_2025.jsonl

import sys, json, pathlib
from datetime import datetime

REQUIRED = ("string", "number", "symbol")

def is_iso8601(ts: str) -> bool:
    try:
        # accepts "2025-09-15T20:27:57+02:00" and Z if present
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return True
    except Exception:
        return False

def is_nonempty_symbol(s: str) -> bool:
    # keep it timeless & tolerant: any non-empty unicode is fine (incl. 𒀭)
    return isinstance(s, str) and len(s.strip()) > 0

def validate_line(line: str, lineno: int):
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as e:
        return (False, f"line {lineno}: invalid JSON: {e}")

    # required keys
    for k in REQUIRED:
        if k not in obj:
            return (False, f"line {lineno}: missing key '{k}'")

    # basic type checks
    if not isinstance(obj["string"], str):
        return (False, f"line {lineno}: 'string' must be a string")

    if not isinstance(obj["number"], str) or not is_iso8601(obj["number"]):
        return (False, f"line {lineno}: 'number' must be ISO-8601 timestamp")

    if not is_nonempty_symbol(obj["symbol"]):
        return (False, f"line {lineno}: 'symbol' must be a non-empty unicode glyph")

    return (True, None)

def main():
    if len(sys.argv) != 2:
        print("usage: python3 kernel/validate_trinity.py <ledger.jsonl>")
        sys.exit(2)

    path = pathlib.Path(sys.argv[1])
    if not path.exists():
        print(f"error: file not found: {path}")
        sys.exit(2)

    total = ok = 0
    errors = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            total += 1
            good, err = validate_line(line, lineno)
            if good:
                ok += 1
            else:
                errors.append(err)

    if errors:
        print("❌ ledger validation failed")
        for e in errors:
            print(" -", e)
        print(f"summary: {ok}/{total} lines valid")
        sys.exit(1)

    print(f"✅ ledger valid: {ok}/{total} lines")
    sys.exit(0)

if __name__ == "__main__":
    main()
