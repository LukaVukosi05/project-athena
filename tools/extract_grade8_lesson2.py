"""Compile Grade 8 Lesson 2 from the approved, hashed Gold Pack."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from extract_grade8_lesson1 import (
    SOURCE, EXPECTED_HASH, after, between, inline, lines_from_docx,
    value,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "backend/app/curriculum/grade8/generated/lesson_02.json"


def numbered_bank(section: list[str], kind: str, expected: int) -> list[dict]:
    positions = [(i, line.removeprefix("Stable ID: ")) for i, line in enumerate(section)
                 if re.fullmatch(rf"Stable ID: g8-ae-l02-{kind}\d{{2}}", line)]
    if len(positions) != expected:
        raise ValueError(f"Expected {expected} {kind} IDs, found {len(positions)}")
    rows = []
    for offset, (index, stable_id) in enumerate(positions):
        number = offset + 1
        heading = next(line for line in reversed(section[:index]) if re.match(rf"^{number}\.\s+", line))
        end = positions[offset + 1][0] - 1 if offset + 1 < len(positions) else len(section)
        chunk = section[index + 1:end]
        solution_start = chunk.index("Complete solution") + 1
        solution_end = next((i for i in range(solution_start, len(chunk)) if chunk[i].startswith("Misconception tags:")), len(chunk))
        tag = next((line for line in chunk if line.startswith("Misconception tags:")), "")
        rows.append({"id": stable_id, "number": number, "prompt": re.sub(r"^\d+\.\s+", "", heading),
                     "marks": int(value(chunk, "Marks")), "answer": inline(chunk, "Answer"),
                     "solution": chunk[solution_start:solution_end],
                     "misconception_tags": [item.strip() for item in tag.partition(":")[2].split(",") if item.strip()]})
    return rows


def worked_examples(section: list[str]) -> list[dict]:
    positions = [i for i, line in enumerate(section) if re.match(r"Worked example \d+: ", line)]
    if len(positions) != 15:
        raise ValueError(f"Expected 15 worked examples, found {len(positions)}")
    rows = []
    for offset, start in enumerate(positions):
        chunk = section[start:positions[offset + 1] if offset + 1 < len(positions) else len(section)]
        number, prompt = re.match(r"Worked example (\d+): (.+)", chunk[0]).groups()
        stable_id = next(line for line in chunk if re.fullmatch(r"g8-ae-l02-w\d{2}", line))
        pos = chunk.index(stable_id)
        memo_start = chunk.index("Complete memo") + 1
        memo_end = next(i for i in range(memo_start, len(chunk)) if chunk[i].startswith("Misconception tags:"))
        sequence_start = chunk.index("Deterministic teaching sequence") + 1
        verification_index = next(i for i in range(sequence_start, len(chunk)) if chunk[i].startswith("Verification:"))
        rows.append({
            "id": stable_id,
            "number": int(number),
            "prompt": prompt,
            "difficulty": chunk[pos + 1].casefold(),
            "cognitive_level": chunk[pos + 2].casefold().replace(" ", "_"),
            "marks": int(chunk[pos + 3]),
            "answer": inline(chunk, "Learner-facing answer"),
            "memo": chunk[memo_start:memo_end],
            "misconception_tags": [tag.strip() for tag in inline(chunk, "Misconception tags").split(",")],
            "renderer": inline(chunk, "Renderer"),
            "question_data": inline(chunk, "Question data"),
            "initial_state": inline(chunk, "Initial state"),
            "teaching_sequence": chunk[sequence_start:verification_index],
            "verification": chunk[verification_index].split(":", 1)[1].strip(),
            "runtime_rule": inline(chunk, "Runtime rule"),
        })
    return rows


def compile_lesson() -> dict:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != EXPECTED_HASH:
        raise ValueError(f"Gold Pack hash mismatch: {digest}")
    all_lines = lines_from_docx(SOURCE)
    lines = all_lines[all_lines.index("Lesson 2 Equations by inspection"):all_lines.index("Lesson 3 Additive inverse equations")]
    vocab = between(lines, "Vocabulary", "Concept teaching")[2:]
    misconceptions = between(lines, "Misconception diagnosis and repair", "Worked example bank")[3:]
    diagnostic = between(lines, "Entry diagnostic", "Misconception diagnosis and repair")
    payload = {
        "source_document": SOURCE.name,
        "source_sha256": digest,
        "id": value(lines, "Stable lesson ID"),
        "title": lines[0].removeprefix("Lesson 2 "),
        "estimated_minutes": int(re.search(r"\d+", value(lines, "Estimated time")).group()),
        "mastery_threshold": int(value(lines, "Mastery threshold").removesuffix("%")) / 100,
        "objective": after(lines, "Learning objective"),
        "why_it_matters": after(lines, "Why it matters"),
        "prerequisites": between(lines, "Prerequisites", "Vocabulary"),
        "vocabulary": [{"term": vocab[i], "meaning": vocab[i + 1]} for i in range(0, len(vocab), 2)],
        "concept_teaching": between(lines, "Concept teaching", "Entry diagnostic"),
        "entry_diagnostic": {key.casefold().replace(" ", "_"): value(diagnostic, key) for key in ("Prompt", "Answer", "Failure route")},
        "misconceptions": [{"tag": misconceptions[i], "diagnosis": misconceptions[i + 1], "repair": misconceptions[i + 2]} for i in range(0, len(misconceptions), 3)],
        "worked_examples": worked_examples(between(lines, "Worked example bank", "Independent practice")),
        "practice_questions": numbered_bank(between(lines, "Independent practice", "Mastery assessment"), "p", 15),
        "mastery_questions": numbered_bank(between(lines, "Mastery assessment", "Reteaching rules"), "m", 5),
        "repair_rules": between(lines, "Reteaching rules", "Parallel reassessment"),
        "reassessment_questions": numbered_bank(between(lines, "Parallel reassessment", "Lesson summary"), "r", 3),
        "summary": between(lines, "Lesson summary", "Implementation acceptance checklist"),
    }
    ids = [row["id"] for kind in ("worked_examples", "practice_questions", "mastery_questions", "reassessment_questions") for row in payload[kind]]
    if len(ids) != 38 or len(set(ids)) != 38:
        raise ValueError("Lesson 2 requires 38 unique source question IDs")
    return payload


if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(compile_lesson(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)
