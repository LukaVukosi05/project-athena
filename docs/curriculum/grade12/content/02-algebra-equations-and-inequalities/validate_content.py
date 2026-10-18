"""Deterministic authoring QA for Topic 2 Lessons 1-3.

This script validates source documents only. It is not imported by Athena runtime code.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
LESSONS = [ROOT / f"lesson-{number:02}.md" for number in range(1, 4)]
EXPECTED_COGNITION = {"K": 14, "R": 25, "C": 22, "P": 11}
ALLOWED_EVENTS = {
    "focus", "dim", "reveal", "write", "expand", "factor", "substitute",
    "apply_both_sides", "cancel_factor", "compare", "group",
    "mark_restriction", "checkpoint", "verify",
}


def multiply(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def validate_documents() -> None:
    all_ids: list[str] = []
    cognition = {key: 0 for key in EXPECTED_COGNITION}
    expected_categories = {
        "Diagnostic": 4,
        "Guided": 6,
        "Independent and mixed": 10,
        "Misconception/error analysis": 2,
        "Original exam-style": 2,
    }

    for lesson in LESSONS:
        text = lesson.read_text(encoding="utf-8")
        ids = re.findall(r"\*\*(g12-aei-l\d{2}-[dgime]\d{2})\s*\|", text)
        assert len(ids) == 24, f"{lesson.name}: expected 24 items, got {len(ids)}"
        all_ids.extend(ids)

        for level in cognition:
            cognition[level] += len(re.findall(rf"\|\s*{level}\s*\|\s*\d+", text))

        for heading, expected in expected_categories.items():
            start = text.index(f"### {heading}")
            following = text[start:]
            end = following.find("\n### ", 5)
            section = following if end == -1 else following[:end]
            count = len(re.findall(r"^\d+\. \*\*g12-aei", section, re.MULTILINE))
            assert count == expected, f"{lesson.name} {heading}: {count} != {expected}"

        for event in re.findall(r"type:\s*([a-z_]+)", text):
            assert event in ALLOWED_EVENTS, f"{lesson.name}: unregistered event {event}"
        assert "javascript:" not in text.lower()
        assert "eval(" not in text.lower()

    assert len(all_ids) == len(set(all_ids)) == 72
    assert cognition == EXPECTED_COGNITION, (cognition, EXPECTED_COGNITION)


def validate_mathematics() -> None:
    # Coefficients are highest degree first.
    identities = [
        ([12, -18, 0, 0], [6, 0, 0], [2, -3]),
        ([2, -7, 3], [2, -1], [1, -3]),
        ([3, 11, 6], [3, 2], [1, 3]),
        ([2, 1, -6], [2, -3], [1, 2]),
        ([6, -1, -2], [3, -2], [2, 1]),
    ]
    for original, left, right in identities:
        assert multiply(left, right) == original

    assert Fraction(5, 6) - Fraction(3, 4) == Fraction(1, 12)
    assert Fraction(-3, 5) / Fraction(9, 10) == Fraction(-2, 3)
    assert Fraction(27, 3) - Fraction(16, 2) == 1

    for x in (-5, -2, 0, 1, 5):
        if x != 3:
            assert Fraction(x * x - 9, x - 3) == x + 3
    for x in (-4, 0, 3, 5):
        if x not in (-1, 1):
            left = Fraction(2, x - 1) - Fraction(3, x + 1)
            right = Fraction(5 - x, x * x - 1)
            assert left == right


if __name__ == "__main__":
    validate_documents()
    validate_mathematics()
    print("Topic 2 authoring QA passed: 3 lessons, 72 items, semantic events and core mathematics.")
