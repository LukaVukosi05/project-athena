import json
import importlib.util
from pathlib import Path
import pytest
from pydantic import ValidationError

from app.curriculum.schemas import TimelineEvent


def test_question_first_semantic_events_are_registered_and_non_executable():
    for event_type in ("show_question", "set_goal", "focus", "dim", "show_operation", "apply_both_sides", "cancel", "simplify", "substitute", "verify", "complete"):
        payload={"at_ms":0,"type":event_type}
        if event_type=="apply_both_sides": payload["targets"]=["left-side","right-side"]
        assert TimelineEvent(**payload).type==event_type
    with pytest.raises(ValidationError):
        TimelineEvent(at_ms=0,type="execute_javascript")


def test_apply_both_sides_requires_both_equation_sides():
    with pytest.raises(ValidationError,match="both equation sides"):
        TimelineEvent(at_ms=0,type="apply_both_sides",targets=["left-side"])


def test_balance_prototype_uses_real_states_and_delays_the_answer():
    from app.curriculum.grade12.lessons.algebra_equations_inequalities import ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS

    board = ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS[0].whiteboard_questions[0].whiteboard
    states = [board.initial_expression, *[step.after_expression for step in board.steps]]
    assert states[:3] == ["3x + 7 = 22"] * 3
    assert states[3:] == [
        "3x + 7 - 7 = 22 - 7", "3x = 15", "3x / 3 = 15 / 3",
        "x = 5", "3(5) + 7 = 22", "15 + 7 = 22", "22 = 22 ✓",
    ]
    assert all("Structure:" not in value and "Selected method:" not in value for value in states)
    assert "x = 5" not in " ".join(states[:6])
    assert any(event.type == "apply_both_sides" for event in board.steps[2].events)


def test_golden_balance_example_contract_is_unchanged():
    from app.curriculum.grade12.lessons.algebra_equations_inequalities import ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS

    expected = json.loads((Path(__file__).parent / "fixtures" / "g12_algebra_01_w01_golden.json").read_text(encoding="utf-8"))
    question = ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS[0].whiteboard_questions[0]
    actual = {
        "lesson_id": "g12-algebra-01", "question_id": question.id,
        "question": question.whiteboard.problem, "answer": question.answer,
        "steps": [[
            step.operation.type, step.animation_template, step.before_expression,
            step.working_expression, step.after_expression, step.duration_ms,
            next(event.text for event in step.events if event.type == "caption"),
        ] for step in question.whiteboard.steps],
    }
    assert actual == expected


def test_second_balance_example_is_animated_not_memo_templated():
    from app.curriculum.grade12.lessons.algebra_equations_inequalities import ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS

    board = ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS[0].whiteboard_questions[1].whiteboard
    states = [board.initial_expression, *[step.after_expression for step in board.steps]]
    assert states[3:] == ["5x - 4 + 4 = 11 + 4", "5x = 15", "5x / 5 = 15 / 5", "x = 3", "5(3) - 4 = 11", "15 - 4 = 11", "11 = 11 ✓"]
    assert not any(label in value for value in states for label in ("Structure:", "Selected method:", "Apply:", "Conclusion:"))


def test_golden_second_balance_example_contract_is_unchanged():
    from app.curriculum.grade12.lessons.algebra_equations_inequalities import ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS

    expected = json.loads((Path(__file__).parent / "fixtures" / "g12_algebra_01_w02_golden.json").read_text(encoding="utf-8"))
    question = ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS[0].whiteboard_questions[1]
    actual = {
        "lesson_id": "g12-algebra-01", "question_id": question.id,
        "question": question.whiteboard.problem, "answer": question.answer,
        "steps": [[
            step.operation.type, step.animation_template, step.before_expression,
            step.working_expression, step.after_expression, step.duration_ms,
            next(event.text for event in step.events if event.type == "caption"),
        ] for step in question.whiteboard.steps],
    }
    assert actual == expected


def test_every_active_grade_12_whiteboard_passes_animation_audit():
    from app.curriculum.repository import curriculum_repository

    audit_path = Path(__file__).parents[2] / "tools" / "audit_whiteboard_animations.py"
    spec = importlib.util.spec_from_file_location("whiteboard_animation_audit", audit_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    failures = []
    grade = curriculum_repository.get_grade("grade-12")
    for topic in grade.topics:
        for subtopic in topic.subtopics:
            for lesson in subtopic.lessons:
                for question in lesson.whiteboard_questions:
                    result = module.animation_assessment(question)
                    if not result["meaningful"]:
                        failures.append(f"{topic.id} / {lesson.id} / {question.id} / {result['reason']}")
    assert not failures, "\n".join(failures)
