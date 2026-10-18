"""Generate the complete Grade 12 whiteboard-animation coverage report."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.curriculum.repository import curriculum_repository
from app.whiteboard.registry import registry
from app.visualization.registry import CATALOGUE

FRONTEND_REGISTRY = (ROOT / "frontend/js/whiteboard/animation-registry.js").read_text(encoding="utf-8")
MEMO_LABELS = ("Structure:", "Selected method:", "Operation selected for:", "Apply:", "Conclusion:")


def animation_assessment(question):
    board = question.whiteboard
    object_ids = {item.id for item in board.semantic_objects}
    reasons: list[str] = []
    operations = [step.operation.type for step in board.steps]
    event_counts = [len(step.events) for step in board.steps]
    missing_targets = sorted({target for step in board.steps for event in step.events for target in event.targets if target not in object_ids})
    backend_registered = all(operation in registry._operations for operation in operations)
    frontend_registered = all(operation in FRONTEND_REGISTRY for operation in operations)
    template_registered = board.visualization is None or (board.visualization.type, board.visualization.template) in CATALOGUE
    final = (question.answer or "").strip()
    initial = f"{board.problem} {board.initial_expression} {board.steps[0].before_expression}"
    # A short answer token may legitimately occur among the givens (for example
    # d=0 or r=1/2). Only flag an authored answer when the complete answer is
    # presented as a result in the opening state.
    final_hidden = not final or not any(marker in initial for marker in (f"Therefore {final}", f"Verified: {final}", f"Answer: {final}"))
    changed_steps = [step for step in board.steps if step.before_expression != step.working_expression or step.working_expression != step.after_expression]
    visible_operations = [step for step in board.steps if step.working_expression and step.working_expression != step.before_expression]
    verification = any("verif" in step.operation.type or any(event.type in {"verify", "verify_original", "verify_financial_sense", "verify_calculus_sense"} for event in step.events) for step in board.steps)
    memo_repetition = sum(any(label in " ".join(filter(None, (step.before_expression, step.working_expression, step.after_expression))) for label in MEMO_LABELS) for step in board.steps)
    if not backend_registered: reasons.append("backend operation validator missing")
    if not frontend_registered: reasons.append("frontend operation renderer missing")
    if not template_registered: reasons.append("visualization template missing")
    if missing_targets: reasons.append(f"event targets missing: {', '.join(missing_targets)}")
    if not any(event_counts): reasons.append("no semantic timeline events")
    if not object_ids: reasons.append("no semantic objects")
    if not changed_steps: reasons.append("all mathematical states are identical")
    if not visible_operations: reasons.append("no visible operation state")
    if not final_hidden: reasons.append("final answer appears in initial state")
    if memo_repetition: reasons.append(f"generic memo template used in {memo_repetition} steps")
    if not verification: reasons.append("no explicit original-task verification")
    meaningful = not reasons
    repair = "None" if meaningful else "; ".join(reasons).replace("generic memo template used", "replace memo factory with operation-family timeline; generic memo template used")
    return {
        "operations": operations, "event_counts": event_counts, "objects": sorted(object_ids),
        "visualization": f"{board.visualization.type}:{board.visualization.template}" if board.visualization else "none",
        "before": all(bool(step.before_expression.strip()) for step in board.steps),
        "working": all(bool((step.working_expression or "").strip()) for step in board.steps),
        "after": all(bool(step.after_expression.strip()) for step in board.steps),
        "distinct": bool(changed_steps and visible_operations), "final_hidden": final_hidden,
        "frontend_registered": frontend_registered, "backend_registered": backend_registered,
        "targets_valid": not missing_targets, "meaningful": meaningful,
        "reason": "; ".join(reasons) or "none", "repair": repair,
    }


def generate() -> str:
    grade = curriculum_repository.get_grade("grade-12")
    rows = []
    for topic in grade.topics:
        for subtopic in topic.subtopics:
            for lesson in subtopic.lessons:
                for question in lesson.whiteboard_questions:
                    board = question.whiteboard
                    audit = animation_assessment(question)
                    rows.append((topic, lesson, question, board, audit))
    failed = sum(not row[-1]["meaningful"] for row in rows)
    out = ["# Grade 12 whiteboard animation audit", "", f"Generated from the authoritative backend repository. Examples inspected: **{len(rows)}**. Examples requiring repair: **{failed}**.", "",
           "| Topic ID | Lesson ID | Lesson title | Example ID | Order | Problem | Representation | Steps | Operations | Events/step | Semantic objects | Visualization | Before | Working | After | Distinct phases | Final hidden | Frontend renderer | Backend validator | Targets valid | Meaningfully animated | Failure reason | Required repair |",
           "|---|---|---|---|---:|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    clean = lambda value: str(value).replace("|", "\\|").replace("\n", " ")
    for topic, lesson, question, board, audit in rows:
        out.append("| " + " | ".join(map(clean, (
            topic.id, lesson.id, lesson.title, question.id, question.order, board.problem,
            board.representation, len(board.steps), ", ".join(audit["operations"]),
            ", ".join(map(str, audit["event_counts"])), f"{len(audit['objects'])}: {', '.join(audit['objects'])}",
            audit["visualization"], audit["before"], audit["working"], audit["after"], audit["distinct"],
            audit["final_hidden"], audit["frontend_registered"], audit["backend_registered"],
            audit["targets_valid"], audit["meaningful"], audit["reason"], audit["repair"],
        ))) + " |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    target = ROOT / "docs/whiteboard-animation-audit.md"
    target.write_text(generate(), encoding="utf-8")
    print(target)
