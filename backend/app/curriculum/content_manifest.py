"""Source-derived curriculum readiness and availability manifest.

This module deliberately separates source authoring from runtime publication.
The Grades 8--11 master packs and the Grade 12 requirements document were not
present in the repository when this manifest was created, so no topic names or
lesson counts are invented for those sources.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Iterable

from app.curriculum.schemas import GradeCurriculum, Lesson


class ReadinessState(StrEnum):
    ROADMAP = "roadmap"
    SPECIFIED = "specified"
    ANCHORED = "anchored"
    AUTHORED = "authored"
    VERIFIED = "verified"
    PUBLISHED = "published"


USABLE_STATES = frozenset({ReadinessState.VERIFIED, ReadinessState.PUBLISHED})

# These are deliberate release decisions carried forward from the protected
# Grade 12 baseline. New lessons use ``Lesson.release_approved`` directly.
EXPLICITLY_RELEASED_LESSON_IDS = frozenset({
    "g12-sequences-series-01",
    "g12-finance-01",
    "g12-calculus-01",
    "g12-algebra-01",
    "g12-statistics-01",
    "g12-analytical-geometry-01",
})


def release_gate_passes(lesson: Lesson) -> bool:
    """Enforce the explicit runtime release contract for newly published work."""
    if not lesson.release_approved or not lesson.blocks or not lesson.whiteboard_questions:
        return False
    contract = lesson.assessment_contract
    required_blocks = {"concept", "mistake", "practice", "summary"}
    if not required_blocks.issubset({block.type for block in lesson.blocks}):
        return False
    if contract.get("worked_example_count") != len(lesson.whiteboard_questions):
        return False
    if contract.get("answer_hidden_before_submission") is not True or contract.get("progression_threshold") != .8:
        return False
    from app.visualization.registry import CATALOGUE
    for question in lesson.whiteboard_questions:
        board = question.whiteboard
        if not board.visualization or (board.visualization.type, board.visualization.template) not in CATALOGUE:
            return False
        object_ids = {item.id for item in board.semantic_objects}
        if not object_ids or any(
            target not in object_ids
            for step in board.steps
            for event in step.events
            for target in [*event.targets, event.from_target, event.to_target]
            if target
        ):
            return False
    if lesson.id in {"g8-algebraic-equations-01", "g8-algebraic-equations-02"}:
        if lesson.id.endswith("-01"):
            from app.curriculum.grade8 import assessment as bank
        else:
            from app.curriculum.grade8 import assessment_lesson2 as bank
        return (
            len(bank.PRACTICE_BANK) == contract.get("practice_count") == 15
            and len(bank.MASTERY_BANK) == contract.get("mastery_question_count") == 5
            and len(bank.REASSESSMENT_BANK) == contract.get("parallel_reassessment_count") == 3
            and bool(bank.MISCONCEPTION_REPAIRS)
        )
    if lesson.id in {"g8-algebraic-equations-03", "g8-algebraic-equations-04", "g8-algebraic-equations-05", "g8-algebraic-equations-06", "g8-algebraic-equations-07", "g8-algebraic-equations-08"}:
        if lesson.id.endswith("-03"):
            from app.curriculum.grade8 import assessment_lesson3 as bank
        elif lesson.id.endswith("-04"):
            from app.curriculum.grade8 import assessment_lesson4 as bank
        elif lesson.id.endswith("-05"):
            from app.curriculum.grade8 import assessment_lesson5 as bank
        elif lesson.id.endswith("-06"):
            from app.curriculum.grade8 import assessment_lesson6 as bank
        elif lesson.id.endswith("-07"):
            from app.curriculum.grade8 import assessment_lesson7 as bank
        else:
            from app.curriculum.grade8 import assessment_lesson8 as bank
        return (
            len(bank.PRACTICE_BANK) == contract.get("practice_count") == 15
            and len(bank.MASTERY_BANK) == contract.get("mastery_question_count") == 5
            and len(bank.REASSESSMENT_BANK) == contract.get("parallel_reassessment_count") == 3
            and bool(bank.MISCONCEPTION_REPAIRS)
        )
    return True

SOURCE_INVENTORY = (
    {
        "document": "Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx",
        "grade": "8",
        "present": True,
        "topics_described": ["Algebraic Equations"],
        "lessons_expected": 10,
        "fully_authored_lessons": 10,
        "reference_questions": "15 worked examples, 15 independent questions, 5 mastery questions and 3 parallel reassessments per lesson",
        "whiteboard_specifications": "Question-specific algebra renderers and deterministic teaching sequences for every worked example",
        "missing_content": "Runtime question conversion, renderer implementation and independent validation remain.",
        "implementation_status": "catalogue_integrated_runtime_conversion_pending",
    },
    {
        "document": "Project_Athena_Grades_8_9_Master_Education_Pack.docx",
        "grade": "8-9",
        "present": False,
        "topics_described": None,
        "lessons_expected": None,
        "fully_authored_lessons": None,
        "reference_questions": None,
        "whiteboard_specifications": None,
        "missing_content": "Authoritative master document is absent from the repository.",
        "implementation_status": "source_blocked",
    },
    {
        "document": "Project_Athena_Grades_10_11_Master_Education_Pack.docx",
        "grade": "10-11",
        "present": False,
        "topics_described": None,
        "lessons_expected": None,
        "fully_authored_lessons": None,
        "reference_questions": None,
        "whiteboard_specifications": None,
        "missing_content": "Authoritative master document is absent from the repository.",
        "implementation_status": "source_blocked",
    },
    {
        "document": "Project_Athena_Grade_12_Mathematics_Content_Requirements.docx",
        "grade": "12",
        "present": False,
        "topics_described": None,
        "lessons_expected": None,
        "fully_authored_lessons": None,
        "reference_questions": None,
        "whiteboard_specifications": None,
        "missing_content": "Authoritative requirements document is absent; only approved topic packs are registered.",
        "implementation_status": "partially_source_blocked",
    },
    {
        "document": "Project_Athena_Grade12_Topic1_Sequences_and_Series_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Sequences and Series"],
        "lessons_expected": 18,
        "fully_authored_lessons": 18,
        "reference_questions": "12 runtime whiteboard questions per lesson",
        "whiteboard_specifications": "sequence timelines, differences, ratios, sigma and convergence",
        "missing_content": "Independent human verification and final publication review remain.",
        "implementation_status": "runtime_integrated",
    },
    {
        "document": "Project_Athena_Grade12_Topic2_Functions_and_Graphs_Approved_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Functions and Graphs"],
        "lessons_expected": 18,
        "fully_authored_lessons": 18,
        "reference_questions": "Approved source bank; first 3 lessons converted to runtime",
        "whiteboard_specifications": "scaled Cartesian graph families and parameter transformations",
        "missing_content": "Lessons 4-18 require runtime conversion and verification.",
        "implementation_status": "partially_integrated",
    },
    {
        "document": "Project_Athena_Grade12_Topic3_Finance_Growth_and_Decay_Approved_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Finance, Growth and Decay"],
        "lessons_expected": 16,
        "fully_authored_lessons": 16,
        "reference_questions": "Approved source bank; first 3 lessons converted to runtime",
        "whiteboard_specifications": "cash-flow timelines, rates, periods and focal dates",
        "missing_content": "Lessons 4-16 require runtime conversion and verification.",
        "implementation_status": "partially_integrated",
    },
    {
        "document": "Project_Athena_Grade12_Topic4_Differential_Calculus_Approved_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Differential Calculus"],
        "lessons_expected": 24,
        "fully_authored_lessons": 24,
        "reference_questions": "Approved source bank; first 6 lessons converted to runtime",
        "whiteboard_specifications": "secant-to-tangent, derivatives, sign and optimisation visuals",
        "missing_content": "Lessons 7-24 require runtime conversion and verification.",
        "implementation_status": "partially_integrated",
    },
    {
        "document": "Project_Athena_Grade12_Topic5_Algebra_Equations_and_Inequalities_Approved_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Algebra, Equations and Inequalities"],
        "lessons_expected": 18,
        "fully_authored_lessons": 18,
        "reference_questions": "10 guided whiteboards and 12 practice questions per lesson",
        "whiteboard_specifications": "term, factor, branch, restriction and number-line semantics",
        "missing_content": "Independent human verification and final publication review remain.",
        "implementation_status": "runtime_integrated",
    },
    {
        "document": "Project_Athena_Grade12_Topic8_Statistics_and_Regression_Paper2_Approved_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Statistics and Regression"],
        "lessons_expected": 18,
        "fully_authored_lessons": 18,
        "reference_questions": "10 guided whiteboards and 12 practice questions per lesson",
        "whiteboard_specifications": "dataset, ogive, box plot, scatter, regression and outlier canvases",
        "missing_content": "Independent human verification and final publication review remain.",
        "implementation_status": "runtime_integrated",
    },
    {
        "document": "Project_Athena_Grade12_Topic9_Analytical_Geometry_Paper2_Approved_Lesson_Pack.docx",
        "grade": "12",
        "present": True,
        "topics_described": ["Analytical Geometry"],
        "lessons_expected": 16,
        "fully_authored_lessons": 16,
        "reference_questions": "10 guided whiteboards and 12 practice questions per lesson",
        "whiteboard_specifications": "coordinate, gradient, line, circle, radius and tangent canvases",
        "missing_content": "Independent human verification and final publication review remain.",
        "implementation_status": "runtime_integrated",
    },
)


def readiness_for(lesson: Lesson) -> ReadinessState:
    """Return learner-facing readiness without inflating source-only content."""
    if lesson.status.value == "coming_soon":
        return ReadinessState.AUTHORED
    # The current Functions runtime fails the shared whiteboard contract
    # (its read_problem operation and animation template disagree). Keep the
    # source-visible lessons disabled until that authored content is repaired.
    if lesson.id.startswith("g12-functions-"):
        return ReadinessState.AUTHORED
    if not lesson.whiteboard_questions or not lesson.blocks:
        return ReadinessState.SPECIFIED
    if lesson.release_approved:
        return ReadinessState.PUBLISHED if release_gate_passes(lesson) else ReadinessState.AUTHORED
    if lesson.id in EXPLICITLY_RELEASED_LESSON_IDS:
        return ReadinessState.PUBLISHED
    return ReadinessState.VERIFIED


def is_usable(lesson: Lesson) -> bool:
    return readiness_for(lesson) in USABLE_STATES


def manifest_for(grades: Iterable[GradeCurriculum]) -> dict:
    grade_rows = []
    for grade in grades:
        topics = []
        for topic in grade.topics:
            lessons = [lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
            rows = [
                {
                    "id": lesson.id,
                    "order": lesson.order,
                    "title": lesson.title,
                    "readiness": readiness_for(lesson),
                    "runtime_content": bool(lesson.blocks and lesson.whiteboard_questions),
                    "source_document": lesson.source_document,
                }
                for lesson in lessons
            ]
            topics.append({
                "id": topic.id,
                "order": topic.product_order,
                "title": topic.title,
                "paper": topic.paper,
                "expected_lessons": len(lessons),
                "lessons": rows,
            })
        grade_rows.append({"id": grade.id, "grade": grade.grade, "topics": topics})
    return {"states": [state.value for state in ReadinessState], "sources": SOURCE_INVENTORY, "grades": grade_rows}
