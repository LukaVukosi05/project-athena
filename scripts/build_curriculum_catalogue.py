"""Build the checked-in Project Athena runtime catalogue."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.curriculum.catalogue_compiler import OUTPUT, build  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--allow-missing-sources",
        action="store_true",
        help="Write metadata for sources that are present, but report missing masters.",
    )
    args = parser.parse_args()
    discrepancies = build(ROOT, args.output)
    print(f"Wrote deterministic catalogue: {args.output}")
    for discrepancy in discrepancies:
        print(f"DISCREPANCY: {discrepancy}")
    return 0 if not discrepancies or args.allow_missing_sources else 2


if __name__ == "__main__":
    raise SystemExit(main())
