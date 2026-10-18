"""Deterministically convert the approved Paper 2 DOCX tables to runtime JSON.

The packs deliberately use a regular, reviewable table contract.  This tool uses
only the Python standard library so extraction is reproducible in CI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def text(node: ET.Element) -> str:
    return "".join(part.text or "" for part in node.iter(f"{W}t")).strip()


def rows(table: ET.Element) -> list[list[str]]:
    return [
        [text(cell) for cell in row.findall(f"{W}tc")]
        for row in table.findall(f"{W}tr")
    ]


def table_map(table_rows: list[list[str]]) -> dict[str, str]:
    return {row[0]: row[1] for row in table_rows[1:] if len(row) >= 2}


def extract(source: Path) -> dict:
    with zipfile.ZipFile(source) as archive:
        document_xml = archive.read("word/document.xml")
    root = ET.fromstring(document_xml)
    body = root.find(f"{W}body")
    assert body is not None
    elements: list[dict] = []
    for child in body:
        if child.tag == f"{W}p":
            value = text(child)
            if value:
                elements.append({"kind": "paragraph", "text": value})
        elif child.tag == f"{W}tbl":
            value = rows(child)
            elements.append({"kind": "table", "rows": value})

    tables = [item["rows"] for item in elements if item["kind"] == "table"]
    sequence = tables[5]
    lesson_index = {
        row[1]: {"order": int(row[0]), "id": row[1], "title": row[2], "visual_reasoning": row[3]}
        for row in sequence[1:]
    }

    lessons: list[dict] = []
    table_positions = [i for i, item in enumerate(elements) if item["kind"] == "table"]
    for table_number in range(7, len(tables), 7):
        if table_number + 6 >= len(tables) or tables[table_number][0] != ["Field", "Requirement"]:
            break
        requirements = table_map(tables[table_number])
        lesson_id = requirements["Stable ID"]
        base = lesson_index[lesson_id]
        start_position = table_positions[table_number] + 1
        end_position = table_positions[table_number + 1]
        teaching = [
            item["text"] for item in elements[start_position:end_position]
            if item["kind"] == "paragraph"
        ]
        design = table_map(tables[table_number + 1])
        beats = [dict(zip(tables[table_number + 2][0], row)) for row in tables[table_number + 2][1:]]
        guided = [dict(zip(tables[table_number + 3][0], row)) for row in tables[table_number + 3][1:]]
        practice = [dict(zip(tables[table_number + 4][0], row)) for row in tables[table_number + 4][1:]]
        support = [dict(zip(tables[table_number + 5][0], row)) for row in tables[table_number + 5][1:]]
        pass_rows = tables[table_number + 6]
        lessons.append({
            **base,
            "requirements": requirements,
            "teaching": teaching,
            "presentation": {"design": design, "beats": beats},
            "guided_examples": guided,
            "practice_questions": practice,
            "support_contract": support,
            "pass_contract": " ".join(cell for row in pass_rows for cell in row),
        })

    topic_match = re.search(r"Topic(\d+)_", source.name)
    paper = {
        "source": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "document_xml_sha256": hashlib.sha256(document_xml).hexdigest(),
        "topic_number": int(topic_match.group(1)) if topic_match else None,
        "scope": table_map(tables[1]),
        "global_voice_contract": tables[3],
        "sequence": [dict(zip(sequence[0], row)) for row in sequence[1:]],
        "progression": " ".join(cell for row in tables[6] for cell in row),
        "lessons": lessons,
        "assessment_blueprint": tables[7 + len(lessons) * 7] if 7 + len(lessons) * 7 < len(tables) else [],
        "source_review_tables": tables[8 + len(lessons) * 7 :],
        "source_element_count": len(elements),
        "source_table_count": len(tables),
    }
    expected = int(paper["scope"]["Learning path"].split()[0])
    if len(lessons) != expected:
        raise ValueError(f"{source.name}: extracted {len(lessons)} lessons, expected {expected}")
    for lesson in lessons:
        if len(lesson["guided_examples"]) != 10 or len(lesson["practice_questions"]) != 12:
            raise ValueError(f"{source.name}: invalid item counts for {lesson['id']}")
    return paper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = extract(args.source)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{args.source.name}: {len(result['lessons'])} lessons -> {args.output}")


if __name__ == "__main__":
    main()
