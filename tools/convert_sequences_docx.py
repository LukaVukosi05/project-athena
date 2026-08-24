"""Convert the reviewed Sequences and Series DOCX into terminal-readable sources.

The DOCX remains the review artifact. This deterministic stdlib-only importer is
not used at runtime; curriculum Python remains the application authority.
"""
from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Project_Athena_Grade12_Topic1_Sequences_and_Series_Lesson_Pack.docx"
OUTPUT = ROOT / "docs/curriculum/grade12/content/01-sequences-and-series"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def paragraphs() -> list[tuple[str, str]]:
    with ZipFile(SOURCE) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    result = []
    for paragraph in root.findall(".//w:p", NS):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()
        style_node = paragraph.find("./w:pPr/w:pStyle", NS)
        style = style_node.get(f"{{{NS['w']}}}val") if style_node is not None else ""
        if text:
            result.append((style, text))
    return result


def split_lessons(rows: list[tuple[str, str]]) -> tuple[dict[int, list[tuple[str, str]]], list[str]]:
    lessons: dict[int, list[tuple[str, str]]] = {}
    assessment: list[str] = []
    current: int | None = None
    for style, text in rows:
        match = re.match(r"Lesson (\d+)\b", text) if style == "Heading1" else None
        if match:
            current = int(match.group(1))
            lessons[current] = [(style, text)]
        elif current is not None:
            if style == "Heading1" and text.startswith("Appendix"):
                current = None
            else:
                lessons[current].append((style, text))
        if current == 18:
            assessment.append(text)
    return lessons, assessment


def section_text(rows: list[tuple[str, str]], heading: str) -> list[str]:
    active = False
    values = []
    for style, text in rows:
        if style == "Heading2":
            active = text == heading
            continue
        if active:
            values.append(text)
    return values


def lesson_markdown(number: int, rows: list[tuple[str, str]]) -> str:
    title = rows[0][1].split("—", 1)[-1].strip()
    duration = next((text for _, text in rows if text.startswith("Duration:")), "Duration: 50 min")
    minutes = re.search(r"(\d+)", duration).group(1)
    objective = next((text.split(":", 1)[1].strip() for _, text in rows if text.startswith("Mastery objective:")), title)
    teach = section_text(rows, "Teach the idea")
    whiteboard = section_text(rows, "Whiteboard sequence")
    worked = section_text(rows, "Worked examples")
    practice = section_text(rows, "Independent practice and answer check")
    prerequisite = [] if number == 1 else [f"g12-sequences-series-{number - 1:02}"]
    front = f"""---
id: g12-sequences-series-{number:02}
grade: 12
subject: mathematics
topic: sequences-and-series
lesson_number: {number}
title: "{title}"
paper: 1
term: 1
duration_minutes: {minutes}
mastery_threshold: 80
prerequisites: {prerequisite}
caps_outcomes: [patterns-sequences-series]
cognitive_levels: [knowledge, routine, complex, problem_solving]
status: draft
source_document: Project_Athena_Grade12_Topic1_Sequences_and_Series_Lesson_Pack.docx
---

# {title}

## Learning objective

{objective}

## Prerequisite diagnostic

Check the prerequisite concepts listed in the source teaching sequence before beginning the worked examples.

## Full concept explanation

{' '.join(teach)}

## Vocabulary and notation

Use the notation and mathematical vocabulary introduced in the concept explanation exactly as written.

## Whiteboard teaching sequence

"""
    board = "\n".join(f"- {line}" for line in whiteboard)
    examples = "\n".join(f"- {line}" for line in worked)
    questions = "\n".join(f"- {line}" for line in practice)
    return front + board + f"""

## Worked examples

{examples}

## Misconception diagnosis and repair

The misconception-repair statements in the worked examples are part of the authored lesson and must be discussed explicitly.

## Independent practice

{questions}

## Exam-style questions

Use the unfamiliar and integrated items in the authored practice and assessment sections without copying past-paper wording.

## Complete answers and marking guidance

The answer/expected-conclusion entries above are the source answer key. Award method credit for correct structure and substitution.

## Mastery and reteaching rules

Mastery requires 80%. Diagnose the first incorrect reasoning transition, reteach it visually, and reassess with a different example.
"""


def main() -> None:
    rows = paragraphs()
    lessons, assessment = split_lessons(rows)
    if sorted(lessons) != list(range(1, 19)):
        raise RuntimeError("Expected all 18 lessons in the source pack")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "topic.yaml").write_text(
        "id: sequences-and-series\ngrade: 12\nsubject: mathematics\npaper: 1\nterm: 1\n"
        "title: Patterns, Sequences and Series\nlesson_count: 18\nmastery_threshold: 80\n"
        f"source_document: {SOURCE.name}\nstatus: draft\n",
        encoding="utf-8",
    )
    for number, lesson_rows in lessons.items():
        (OUTPUT / f"lesson-{number:02}.md").write_text(lesson_markdown(number, lesson_rows), encoding="utf-8")
    (OUTPUT / "assessment.md").write_text("# Mastery assessment\n\n" + "\n\n".join(assessment), encoding="utf-8")
    corrections = OUTPUT / "content-corrections.md"
    if not corrections.exists():
        corrections.write_text("# Content corrections\n\nNo verified source-answer corrections recorded yet.\n", encoding="utf-8")


if __name__ == "__main__":
    main()
