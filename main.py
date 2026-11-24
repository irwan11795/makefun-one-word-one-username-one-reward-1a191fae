#!/usr/bin/env python3
"""One Word, One Username, One Reward — make.fun entry.

Writes the entrant's own make.fun handle, "meguri", as a single word
to /output/entry.txt (via the MAKEFUN_OUTPUT_DIR fallback chain).
Python 3.13 standard library only, deterministic, no network.
"""

import os
import sys
from pathlib import Path

ENTRY = "meguri"


def candidate_dirs():
    """Yield output directories in priority order."""
    seen = []
    env = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env:
        seen.append(Path(env))
    seen.append(Path("/output"))
    seen.append(Path(__file__).resolve().parent / "output")
    seen.append(Path(os.environ.get("TMPDIR", "/tmp")))
    return seen


def validate(entry):
    """Kit gate: UTF-8, 1-30 characters, not only whitespace."""
    if not isinstance(entry, str) or not entry:
        print("error: entry must be a non-empty string", file=sys.stderr)
        return False
    if not entry.strip():
        print("error: entry must not be only whitespace", file=sys.stderr)
        return False
    if len(entry) > 30:
        print("error: entry exceeds 30 characters", file=sys.stderr)
        return False
    try:
        entry.encode("utf-8")
    except UnicodeEncodeError:
        print("error: entry is not valid UTF-8", file=sys.stderr)
        return False
    return True


def write_entry():
    """Try each candidate dir; return the path written, or None."""
    for directory in candidate_dirs():
        try:
            directory.mkdir(parents=True, exist_ok=True)
            target = directory / "entry.txt"
            target.write_text(ENTRY, encoding="utf-8", newline="")
            return target
        except OSError:
            continue
    return None


def main():
    if not validate(ENTRY):
        return 1
    target = write_entry()
    if target is None:
        print("error: could not write entry.txt to any candidate directory",
              file=sys.stderr)
        return 1
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
