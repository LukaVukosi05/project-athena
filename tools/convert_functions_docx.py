"""Extract the approved Functions and Graphs DOCX into reviewable Markdown.

The DOCX remains the approval artifact. Runtime Python is authored separately.
"""
from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Project_Athena_Grade12_Topic2_Functions_and_Graphs_Approved_Lesson_Pack.docx"
OUTPUT = ROOT / "docs/curriculum/grade12/content/02-functions-and-graphs"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def blocks():
    with ZipFile(SOURCE) as archive:
        body = ET.fromstring(archive.read("word/document.xml")).find("w:body", NS)
    result = []
    for child in body:
        kind = child.tag.rsplit("}", 1)[-1]
        if kind == "p":
            text = "".join(node.text or "" for node in child.findall(".//w:t", NS)).strip()
            style = child.find("./w:pPr/w:pStyle", NS)
            style = style.get(f"{{{NS['w']}}}val") if style is not None else ""
            if text:
                result.append(("p", style, text))
        elif kind == "tbl":
            rows = []
            for row in child.findall("./w:tr", NS):
                rows.append([" ".join("".join(t.text or "" for t in cell.findall(".//w:t", NS)).split()) for cell in row.findall("./w:tc", NS)])
            result.append(("table", "", rows))
    return result


def markdown(items):
    out = []
    for kind, style, value in items:
        if kind == "table":
            width = max(map(len, value))
            rows = [row + [""] * (width - len(row)) for row in value]
            out.extend(["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"])
            out.extend("| " + " | ".join(row) + " |" for row in rows[1:])
        elif style == "Heading1": out.append("# " + value)
        elif style == "Heading2": out.append("## " + value)
        elif style.startswith("List"): out.append("- " + value)
        else: out.append(value)
        out.append("")
    return "\n".join(out).strip() + "\n"


def main():
    items = blocks()
    starts = [(i, int(m.group(1))) for i, item in enumerate(items) if item[0] == "p" and item[1] == "Heading1" and (m := re.match(r"Lesson (\d+)\b", item[2]))]
    assert [number for _, number in starts] == list(range(1, 19))
    appendix = next(i for i, item in enumerate(items) if item[0] == "p" and item[1] == "Heading1" and item[2].startswith("Appendix A"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    titles = []
    for pos, (start, number) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else appendix
        section = items[start:end]
        heading = section[0][2]
        title = heading.split("—", 1)[-1].strip()
        titles.append(title)
        duration = next(item[2] for item in section if item[0] == "p" and item[2].startswith("Duration:"))
        minutes = int(re.search(r"\d+", duration).group())
        objective = next(item[2].split(":", 1)[1].strip() for item in section if item[0] == "p" and item[2].startswith("Mastery objective:"))
        front = f"""---
id: g12-functions-{number:02}
grade: 12
subject: mathematics
topic: functions-graphs
lesson_number: {number}
title: "{title}"
paper: 1
term: 1
duration_minutes: {minutes}
mastery_threshold: 80
prerequisites: {[] if number == 1 else [f'g12-functions-{number-1:02}']}
status: {'teacher_review_required' if number <= 3 else 'coming_soon'}
source_document: {SOURCE.name}
---

## Mastery objective

{objective}

"""
        (OUTPUT / f"lesson-{number:02}.md").write_text(front + markdown(section[1:]), encoding="utf-8")
    manifest = "\n".join(f"  - {{order: {i}, id: g12-functions-{i:02}, title: \"{title}\", status: {'teacher_review_required' if i <= 3 else 'coming_soon'}}}" for i, title in enumerate(titles, 1))
    (OUTPUT / "topic.yaml").write_text(f"""id: functions-graphs
title: Functions and Graphs
grade: 12
paper: 1
product_order: 2
term: 1
mastery_threshold: 80
source_document: {SOURCE.name}
lessons:
{manifest}
""", encoding="utf-8")
    appendices = markdown(items[appendix:])
    (OUTPUT / "source-register.md").write_text("# Source register and appendices\n\n" + appendices, encoding="utf-8")
    (OUTPUT / "assessment-blueprint.yaml").write_text("""status: evidence_mapping_from_approved_pack
paper_files_present_locally: false
warning: Page-level independent verification requires official Paper 1 papers and matching memoranda.
evidence:
  - {year: 2020, paper: 1, skills: [quadratic features, straight lines, transformations, intersections, graph area, exponential and inverse interpretation]}
  - {year: 2022, paper: 1, skills: [parameters, ranges, inverse relationships, intercepts, graph distances]}
  - {year: 2023, paper: 1, skills: [exponential transformations, inverse logarithms, parabola and hyperbola features, inequalities, tangency]}
  - {year: 2024, paper: 1, skills: [exponential parameters and range, inverse coordinates, hyperbola transformations, interval solutions]}
""", encoding="utf-8")
    (OUTPUT / "content-corrections.md").write_text("# Content corrections\n\nNo mathematical corrections recorded during initial extraction.\n", encoding="utf-8")


if __name__ == "__main__":
    main()
