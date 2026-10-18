"""Deterministically compile authoring sources into runtime catalogue metadata.

DOCX files are inspected only by this build step. HTTP requests consume the
checked-in JSON produced here and never open an authoring document.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

from app.curriculum.content_manifest import readiness_for
from app.curriculum.grade12 import GRADE_12
from app.curriculum.grade8 import GRADE_8
from app.curriculum.grade_shells import SOURCE_BLOCKED_GRADES


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).with_name("generated") / "catalogue.json"
MASTER_SOURCE_PATTERNS = {
    "grades-8-9": re.compile(r"grades?[_ -]?8[_ -]?9.*master.*education.*pack", re.I),
    "grades-10-11": re.compile(r"grades?[_ -]?10[_ -]?11.*master.*education.*pack", re.I),
    "grade-12-requirements": re.compile(r"grade[_ -]?12.*mathematics.*content.*requirements", re.I),
}
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def locate_sources(root: Path = ROOT) -> dict[str, Path]:
    documents = sorted(root.rglob("*.docx"), key=lambda path: path.name.casefold())
    located: dict[str, Path] = {}
    for key, pattern in MASTER_SOURCE_PATTERNS.items():
        match = next((path for path in documents if pattern.search(path.stem)), None)
        if match:
            located[key] = match
    return located


def extract_docx_lines(path: Path) -> list[str]:
    """Return document text in XML order, including table-cell paragraphs."""
    with zipfile.ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
    lines: list[str] = []
    for paragraph in root.iter(f"{WORD_NS}p"):
        text = "".join(node.text or "" for node in paragraph.iter(f"{WORD_NS}t")).strip()
        if text:
            lines.append(" ".join(text.split()))
    return lines


def _source_row(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "document": path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "paragraph_count": len(extract_docx_lines(path)),
    }


def compile_catalogue(root: Path = ROOT) -> tuple[dict, list[str]]:
    located = locate_sources(root)
    authoring_sources = sorted(
        (path for path in root.rglob("*.docx") if path.name.casefold().startswith("project_athena")),
        key=lambda path: path.name.casefold(),
    )
    discrepancies = [
        f"missing required source: {key}"
        for key in MASTER_SOURCE_PATTERNS
        if key not in located
    ]
    grades = []
    seen_topic_ids: set[str] = set()
    seen_lesson_ids: set[str] = set()
    for grade in (GRADE_8, *SOURCE_BLOCKED_GRADES, GRADE_12):
        topics = []
        for topic in sorted(grade.topics, key=lambda item: item.product_order):
            if topic.id in seen_topic_ids:
                discrepancies.append(f"duplicate topic id: {topic.id}")
            seen_topic_ids.add(topic.id)
            lessons = sorted(
                (lesson for subtopic in topic.subtopics for lesson in subtopic.lessons),
                key=lambda item: item.order,
            )
            for lesson in lessons:
                if lesson.id in seen_lesson_ids:
                    discrepancies.append(f"duplicate lesson id: {lesson.id}")
                seen_lesson_ids.add(lesson.id)
            expected = len(lessons)
            if expected != len({lesson.order for lesson in lessons}):
                discrepancies.append(f"lesson order/count mismatch: {grade.id}/{topic.id}")
            topics.append({
                "topic_id": topic.id,
                "topic_number": topic.product_order,
                "title": topic.title,
                "paper": topic.paper,
                "expected_lesson_count": expected,
                "status": topic.status.value,
                "lessons": [{
                    "lesson_id": lesson.id,
                    "position": lesson.order,
                    "title": lesson.title,
                    "status": readiness_for(lesson).value,
                    "duration_minutes": lesson.estimated_minutes,
                    "source_document": lesson.source_document,
                } for lesson in lessons],
            })
        grades.append({
            "grade_id": grade.id,
            "title": f"Grade {grade.grade} Mathematics",
            "curriculum": "CAPS",
            "topics": topics,
        })
    payload = {
        "schema_version": 1,
        "source_documents": [_source_row(path) for path in authoring_sources],
        "grades": grades,
    }
    return payload, discrepancies


def write_catalogue(payload: dict, output: Path = OUTPUT) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(root: Path = ROOT, output: Path = OUTPUT) -> list[str]:
    payload, discrepancies = compile_catalogue(root)
    write_catalogue(payload, output)
    return discrepancies
