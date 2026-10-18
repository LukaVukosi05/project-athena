"""Write the private pre-repair timeline audit used for the Lesson 1 repair."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.curriculum.grade8.teaching_timelines import TEACHING_TIMELINES  # noqa: E402

source_path = ROOT / "backend/app/curriculum/grade8/generated/lesson_01.json"
output_path = ROOT / "artifacts/grade8-algebraic-equations-lesson1/teaching-timeline-repair/internal-audit.md"
source = json.loads(source_path.read_text(encoding="utf-8"))
rows = [
    "# Grade 8 Lesson 1 pre-repair teaching-timeline audit",
    "",
    "This is engineering evidence, not learner content. Before the repair, each Gold Pack authoring direction was copied verbatim into both caption and narration, while the stage used hidden generic `stage-*` targets.",
    "",
    "| Question ID | Step | Current narration | Internal action | Mathematical idea | Required visual change | Replacement learner narration |",
    "|---|---:|---|---|---|---|---|",
]
for question in source["worked_examples"]:
    plan = TEACHING_TIMELINES[question["id"]]
    instructions = question["teaching_sequence"]
    for index, instruction in enumerate(instructions):
        mapped = plan[min(len(plan) - 1, index * len(plan) // len(instructions))]
        clean = lambda value: str(value).replace("|", "\\|").replace("\n", " ")
        rows.append(
            f"| {question['id']} | {index + 1} | {clean(instruction)} | {clean(instruction)} | "
            f"{mapped['action'].replace('_', ' ')} | {clean(mapped['working'])} → {clean(mapped['after'])} | {clean(mapped['narration'])} |"
        )
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"Wrote {sum(len(item['teaching_sequence']) for item in source['worked_examples'])} audited steps to {output_path}")
