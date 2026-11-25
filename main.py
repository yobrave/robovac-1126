#!/usr/bin/env python3
"""rve entry publisher with an explicit result enum."""

import json
import os
from pathlib import Path

BOUNTY_LIMIT = 140


class Result:
    GOOD = "good"
    BAD = "bad"
    GONE = "gone"


def collect():
    entry = Path(__file__).resolve().parent / "entry.txt"
    if not entry.exists():
        return None, Result.GONE
    raw = entry.read_text(encoding="utf-8")
    for row in raw.replace("\r\n", "\n").split("\n"):
        if row.strip():
            return row, Result.GOOD
    return None, Result.BAD


def publish():
    line, status = collect()
    if status != Result.GOOD:
        print(json.dumps({"publish": status}))
        return 1
    if len(line) > BOUNTY_LIMIT or len(line) < 1:
        print(json.dumps({"publish": Result.BAD, "len": len(line),
                          "limit": BOUNTY_LIMIT}))
        return 1
    spot = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    spot.mkdir(parents=True, exist_ok=True)
    (spot / "entry.txt").write_text(line, encoding="utf-8", newline="\n")
    print(json.dumps({"publish": Result.GOOD, "len": len(line)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(publish())
