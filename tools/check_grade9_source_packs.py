"""Structural preflight for Grade 9 Markdown question banks.

Run from any directory: python tools/check_grade9_source_packs.py
This verifies authored source inventory, not mathematical correctness or runtime readiness.
"""

from collections import Counter
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PACKS = sorted((ROOT / "docs/curriculum/grade9/whole-numbers").glob("lesson-*.md"))
EXPECTED = {"W": 15, "P": 15, "M": 5, "R": 3}


def rows(text: str, prefix: str):
    pattern = re.compile(rf"^\| ({prefix}\d{{2}})(?:\s|\||$)")
    return [line.split("|")[1:-1] for line in text.splitlines() if pattern.match(line)]


def check_pack(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures = []
    for prefix, count in EXPECTED.items():
        bank = rows(text, prefix)
        ids = [re.match(rf"{prefix}\d{{2}}", row[0].strip()).group() for row in bank]
        expected = [f"{prefix}{i:02}" for i in range(1, count + 1)]
        if ids != expected:
            failures.append(f"{prefix} IDs expected {expected}; got {ids}")
        for row in bank:
            question_id = row[0].strip().split()[0]
            if prefix == "W":
                if len(row) != 4 or any(not cell.strip() for cell in row):
                    failures.append(f"{question_id}: missing prompt, action or check")
                continue
            if prefix == "P":
                if len(row) != 7:
                    failures.append(f"{question_id}: expected prompt, four options and private key")
                    continue
                options = [cell.strip().strip("`") for cell in row[2:6]]
                answer = row[6]
            else:
                if len(row) != 4:
                    failures.append(f"{question_id}: expected prompt, four options and private key")
                    continue
                options = [part.strip().strip("`") for part in row[2].split(";")]
                answer = row[3]
            if len(options) != 4 or len(set(options)) != 4 or not all(options):
                failures.append(f"{question_id}: options must be four nonempty distinct texts")
            if not re.search(r"\*\*[ABCD]\*\*", answer):
                failures.append(f"{question_id}: missing private A–D key")
            if not answer.strip().split(". ", 1)[-1].strip():
                failures.append(f"{question_id}: missing private answer reason")
    if "no runtime lesson is registered" not in text:
        failures.append("source status must remain explicit until implemented")
    return failures


def main() -> int:
    if not PACKS:
        print("No Grade 9 source packs found", file=sys.stderr)
        return 1
    failed = False
    for path in PACKS:
        failures = check_pack(path)
        print(f"{path.relative_to(ROOT)}: {'FAIL' if failures else 'structural preflight passed'}")
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        failed |= bool(failures)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
