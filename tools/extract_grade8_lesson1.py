"""Compile Grade 8 Algebraic Equations Lesson 1 from its approved DOCX.

This is a build-time authoring tool. Production code reads the generated JSON
and never parses the DOCX on a learner request.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"
OUTPUT = ROOT / "backend/app/curriculum/grade8/generated/lesson_01.json"
EXPECTED_HASH = "69b97ae1d9f85d0f9fb41aad170f6cbc777f2e39844dd6b8d6235bee6c093574"
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def lines_from_docx(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
    lines = []
    for paragraph in root.iter(f"{WORD_NS}p"):
        text = "".join(node.text or "" for node in paragraph.iter(f"{WORD_NS}t")).strip()
        if text:
            lines.append(" ".join(text.split()))
    return lines


def after(lines: list[str], label: str) -> str:
    index = lines.index(label)
    return lines[index + 1]


def value(lines: list[str], label: str) -> str:
    for index, line in enumerate(lines):
        if line == label:
            return lines[index + 1]
        if line.startswith(f"{label}:"):
            return line.split(":", 1)[1].strip()
    raise ValueError(f"Missing field: {label}")


def between(lines: list[str], start: str, end: str) -> list[str]:
    return lines[lines.index(start) + 1:lines.index(end)]


def inline(lines: list[str], prefix: str) -> str:
    return next(line.split(":", 1)[1].strip() for line in lines if line.startswith(f"{prefix}:"))


def numbered_bank(section: list[str], kind: str, expected: int) -> list[dict]:
    id_pattern = re.compile(rf"g8-ae-l01-{kind}(\d{{2}})")
    positions = []
    for index, line in enumerate(section):
        match = id_pattern.fullmatch(line) or id_pattern.fullmatch(line.removeprefix("Stable ID: "))
        if match:
            positions.append((index, match.group(0), int(match.group(1))))
    if len(positions) != expected:
        raise ValueError(f"Expected {expected} {kind} IDs, found {len(positions)}")
    rows = []
    for offset, (id_index, stable_id, number) in enumerate(positions):
        start = 0 if offset == 0 else positions[offset - 1][0] + 1
        # The next numbered question is the paragraph immediately before its
        # stable ID. Exclude that prompt from the current question's solution.
        end = positions[offset + 1][0] - 1 if offset + 1 < len(positions) else len(section)
        prompt_pattern = re.compile(rf"^{number}\.\s+(.+)")
        prompt = next(
            match.group(1)
            for line in reversed(section[start:id_index])
            if (match := prompt_pattern.match(line))
        )
        chunk = section[id_index + 1:end]
        answer = inline(chunk, "Answer")
        solution_start = chunk.index("Complete solution") + 1
        solution_end = next(
            (i for i in range(solution_start, len(chunk)) if chunk[i].startswith(("Misconception tags:", "Reteaching rules", "Parallel reassessment", "Lesson summary"))),
            len(chunk),
        )
        row = {
            "id": stable_id,
            "number": number,
            "prompt": prompt,
            "marks": int(value(chunk, "Marks")) if any(line.startswith("Marks") for line in chunk) else None,
            "answer": answer,
            "solution": chunk[solution_start:solution_end],
            "misconception_tags": [],
        }
        tag_line = next((line for line in chunk if line.startswith("Misconception tags:")), None)
        if tag_line:
            row["misconception_tags"] = [tag.strip() for tag in tag_line.split(":", 1)[1].split(",")]
        rows.append(row)
    return rows


def worked_examples(section: list[str]) -> list[dict]:
    starts = [i for i, line in enumerate(section) if re.match(r"Worked example \d+: ", line)]
    rows = []
    for offset, start in enumerate(starts):
        end = starts[offset + 1] if offset + 1 < len(starts) else len(section)
        chunk = section[start:end]
        number, prompt = re.match(r"Worked example (\d+): (.+)", chunk[0]).groups()
        stable_id = next(
            match.group(0)
            for line in chunk
            if (match := re.search(r"g8-ae-l01-w\d{2}", line))
        )
        id_index = next(i for i, line in enumerate(chunk) if stable_id in line)
        table_values = chunk[id_index + 1:id_index + 4]
        answer = inline(chunk, "Learner-facing answer")
        memo_start = chunk.index("Complete memo") + 1
        memo_end = next(i for i in range(memo_start, len(chunk)) if chunk[i].startswith("Misconception tags:"))
        sequence_start = chunk.index("Deterministic teaching sequence") + 1
        verification_index = next(i for i in range(sequence_start, len(chunk)) if chunk[i].startswith("Verification:"))
        rows.append({
            "id": stable_id,
            "number": int(number),
            "prompt": prompt,
            "difficulty": table_values[0].casefold(),
            "cognitive_level": table_values[1].casefold().replace(" ", "_"),
            "marks": int(table_values[2]),
            "answer": answer,
            "memo": chunk[memo_start:memo_end],
            "misconception_tags": [tag.strip() for tag in inline(chunk, "Misconception tags").split(",")],
            "renderer": inline(chunk, "Renderer"),
            "question_data": inline(chunk, "Question data"),
            "initial_state": inline(chunk, "Initial state"),
            "teaching_sequence": chunk[sequence_start:verification_index],
            "verification": chunk[verification_index].split(":", 1)[1].strip(),
            "runtime_rule": inline(chunk, "Runtime rule"),
        })
    if len(rows) != 15:
        raise ValueError(f"Expected 15 worked examples, found {len(rows)}")
    return rows


def compile_lesson() -> dict:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != EXPECTED_HASH:
        raise ValueError(f"Gold Pack hash mismatch: {digest}")
    all_lines = lines_from_docx(SOURCE)
    start = all_lines.index("Lesson 1 Meaning of equality")
    end = next(i for i in range(start + 1, len(all_lines)) if all_lines[i].startswith("Lesson 2 "))
    lines = all_lines[start:end]
    vocabulary_lines = between(lines, "Vocabulary", "Concept teaching")[2:]
    vocabulary = [
        {"term": vocabulary_lines[i], "meaning": vocabulary_lines[i + 1]}
        for i in range(0, len(vocabulary_lines), 2)
    ]
    misconception_lines = between(lines, "Misconception diagnosis and repair", "Worked example bank")[3:]
    misconceptions = [
        {"tag": misconception_lines[i], "diagnosis": misconception_lines[i + 1], "repair": misconception_lines[i + 2]}
        for i in range(0, len(misconception_lines), 3)
    ]
    worked_section = between(lines, "Worked example bank", "Independent practice")
    practice_section = between(lines, "Independent practice", "Mastery assessment")
    mastery_section = between(lines, "Mastery assessment", "Reteaching rules")
    repair_rules = between(lines, "Reteaching rules", "Parallel reassessment")
    reassessment_section = between(lines, "Parallel reassessment", "Lesson summary")
    payload = {
        "source_document": SOURCE.name,
        "source_sha256": digest,
        "id": value(lines, "Stable lesson ID"),
        "title": lines[0].removeprefix("Lesson 1 "),
        "estimated_minutes": int(re.search(r"\d+", value(lines, "Estimated time")).group()),
        "mastery_threshold": int(value(lines, "Mastery threshold").removesuffix("%")) / 100,
        "objective": after(lines, "Learning objective"),
        "why_it_matters": after(lines, "Why it matters"),
        "prerequisites": between(lines, "Prerequisites", "Vocabulary"),
        "vocabulary": vocabulary,
        "concept_teaching": between(lines, "Concept teaching", "Entry diagnostic"),
        "entry_diagnostic": {
            "prompt": value(between(lines, "Entry diagnostic", "Misconception diagnosis and repair"), "Prompt"),
            "answer": value(between(lines, "Entry diagnostic", "Misconception diagnosis and repair"), "Answer"),
            "failure_route": value(between(lines, "Entry diagnostic", "Misconception diagnosis and repair"), "Failure route"),
        },
        "misconceptions": misconceptions,
        "worked_examples": worked_examples(worked_section),
        "practice_questions": numbered_bank(practice_section, "p", 15),
        "mastery_questions": numbered_bank(mastery_section, "m", 5),
        "repair_rules": repair_rules,
        "reassessment_questions": numbered_bank(reassessment_section, "r", 3),
        "summary": between(lines, "Lesson summary", "Implementation acceptance checklist"),
    }
    all_ids = [item["id"] for name in ("worked_examples", "practice_questions", "mastery_questions", "reassessment_questions") for item in payload[name]]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate Lesson 1 question IDs")
    return payload


def main() -> None:
    payload = compile_lesson()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
