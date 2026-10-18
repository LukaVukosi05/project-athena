"""Contract and mathematical QA for the approved Topic 5 conversion."""
from math import isclose, sqrt

import pytest

from app.curriculum.grade12 import GRADE_12
from app.curriculum.grade12.lessons.algebra_practice import PRACTICE_BANKS
from app.curriculum.schemas import VisualizationInstruction
from app.visualization.registry import validate_visualization
from app.whiteboard.validation import validate_whiteboard
from app.practice.service import mastery_summary


TITLES = [
    "Algebra readiness and equivalence",
    "Factorisation and the zero-product principle",
    "Quadratic equations by factorisation",
    "Quadratic formula",
    "Choosing a quadratic method and rounding",
    "Surd equations and extraneous roots",
    "Equations in quadratic form",
    "Exponential equations and common bases",
    "Linear simultaneous equations",
    "Non-linear simultaneous equations",
    "Quadratic inequalities",
    "Discriminant and nature of roots",
    "Parameter conditions for roots",
    "Algebraic fractions and restrictions",
    "Algebraic proof and reasoning",
    "Contextual modelling",
    "Integrated Paper 1 algebra",
    "Paper 1 algebra mastery assessment",
]


def topic():
    return GRADE_12.topics[4]


def test_topic_five_is_registered_once_after_calculus():
    assert [item.id for item in GRADE_12.topics] == [
        "sequences-series", "functions-graphs", "finance-growth-decay",
        "differential-calculus", "algebra-equations-inequalities",
        "statistics-regression", "analytical-geometry",
    ]
    assert topic().product_order == 5
    assert topic().paper == "Paper 1"
    assert [lesson.id for lesson in topic().subtopics[0].lessons] == [f"g12-algebra-{n:02}" for n in range(1, 19)]
    assert [lesson.title for lesson in topic().subtopics[0].lessons] == TITLES


def test_every_lesson_has_complete_unique_source_authored_banks():
    lessons = topic().subtopics[0].lessons
    assert len(lessons) == 18
    assert all(len(lesson.whiteboard_questions) == 10 for lesson in lessons)
    assert all(len(PRACTICE_BANKS[lesson.id]) == 12 for lesson in lessons)
    whiteboard_ids = [q.id for lesson in lessons for q in lesson.whiteboard_questions]
    practice_ids = [q.id for bank in PRACTICE_BANKS.values() for q in bank]
    assert len(whiteboard_ids) == len(set(whiteboard_ids)) == 180
    assert len(practice_ids) == len(set(practice_ids)) == 216
    assert all(q.id.startswith("G12-ALG-") for bank in PRACTICE_BANKS.values() for q in bank)
    assert all(len(q.hints) == 3 and len(q.worked_solution) == 5 for bank in PRACTICE_BANKS.values() for q in bank)
    assert all(q.worked_solution[-1].verification for bank in PRACTICE_BANKS.values() for q in bank)


def test_algebra_whiteboards_are_registered_deterministic_and_targeted():
    for lesson in topic().subtopics[0].lessons:
        for question in lesson.whiteboard_questions:
            board = question.whiteboard
            assert board.representation == "visual"
            assert board.visualization.type == "algebra"
            assert board.visualization.template == "algebra_reasoning"
            assert [step.step_number for step in board.steps] == list(range(len(board.steps)))
            assert len(board.steps) >= 3
            assert all(step.events and step.state_after for step in board.steps)
            assert all(step.working_expression != step.before_expression for step in board.steps[2:] if step.operation.type != "verification_line")
            validate_whiteboard(board)
    formula = topic().subtopics[0].lessons[3].whiteboard_questions[0].whiteboard
    assert {"discriminant", "candidate", "left-side", "right-side"}.issubset({obj.id for obj in formula.semantic_objects})
    assert any(event.type == "calculate_discriminant" for step in formula.steps for event in step.events)
    rational = topic().subtopics[0].lessons[13].whiteboard_questions[0].whiteboard
    assert any(event.type == "preserve_restriction" for step in rational.steps for event in step.events)
    inequality = topic().subtopics[0].lessons[10].whiteboard_questions[0].whiteboard
    assert any(event.type == "mark_number_line" for step in inequality.steps for event in step.events)


def test_visualization_contract_rejects_unknown_or_excess_parameters():
    board = topic().subtopics[0].lessons[0].whiteboard_questions[0].whiteboard
    validate_visualization(board)
    bad = board.model_copy(update={"visualization": VisualizationInstruction(
        type="algebra", template="algebra_reasoning",
        parameters={**board.visualization.parameters, "javascript": "alert(1)"},
    )})
    with pytest.raises(ValueError, match="Unexpected"):
        validate_visualization(bad)


def test_pack_correction_and_representative_algebra_are_mathematically_valid():
    corrected = PRACTICE_BANKS["g12-algebra-14"][10]
    assert "sqrt(33)" in corrected.accepted_answers[0]
    for root in ((-1 + sqrt(33)) / 2, (-1 - sqrt(33)) / 2):
        assert not isclose(root, -2)
        assert isclose(6 / (root + 2), root - 1)

    # Surd candidates are accepted only when they satisfy the original equation.
    assert isclose(sqrt(4 + 5), 4 - 1)
    assert sqrt(-1 + 5) != -1 - 1

    # Simultaneous ordered pairs retain their pairing and satisfy both equations.
    for x, y in ((2, 3),):
        assert x + y == 5 and 2 * x - y == 1

    # Endpoints come from roots; a region test determines the inequality interval.
    assert (0**2 - 5 * 0 + 6) > 0
    assert (2.5**2 - 5 * 2.5 + 6) < 0
    assert (4**2 - 5 * 4 + 6) > 0


def test_mastery_contract_requires_ten_exam_items_and_explain_back():
    for lesson in topic().subtopics[0].lessons:
        block = next(block for block in lesson.blocks if block.type == "practice")
        mastery = block.data["mastery"]
        assert mastery["minimum_correct"] == 10
        assert mastery["required_exam_question_numbers"] == [11, 12]
        assert mastery["explain_back_required"] is True
        assert mastery["worked_solution_view_is_independent_mastery"] is False
    final = next(block for block in topic().subtopics[0].lessons[-1].blocks if block.type == "practice").data["mastery"]
    assert final["timed_marks"] == 25 and final["minimum_marks"] == 20
    assert final["initial_hints_allowed"] is False
    assert final["parallel_reassessment_required_after_reteach"] is True

    bank=PRACTICE_BANKS["g12-algebra-01"]
    ten={q.id:{"correct":i<10,"first_attempt_correct":i<10,"attempts":1,"hints_used":0,"solution_viewed":False} for i,q in enumerate(bank)}
    assert mastery_summary(ten,bank)["mastered"] is False
    assert mastery_summary(ten,bank)["exam_items_correct"] is False
    passing={q.id:{"correct":i>=2,"first_attempt_correct":i>=2,"attempts":1,"hints_used":0,"solution_viewed":False} for i,q in enumerate(bank)}
    summary=mastery_summary(passing,bank)
    assert summary["mastered"] is True and summary["exam_items_correct"] is True
    assert summary["explain_back_required"] is True
