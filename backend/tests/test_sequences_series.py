from pathlib import Path

import pytest
from pydantic import ValidationError

from app.curriculum.repository import curriculum_repository
from app.curriculum.schemas import TimelineEvent
from app.curriculum.schemas import AccessLevel
from app.visualization.registry import validate_visualization
from app.whiteboard.validation import validate_whiteboard


LESSON_IDS = [f"g12-sequences-series-{number:02}" for number in range(1, 19)]


def lessons():
    return [curriculum_repository.get_lesson(identifier)[2] for identifier in LESSON_IDS]


def test_docx_conversion_contains_all_eighteen_source_lessons():
    root = Path(__file__).parents[2] / "docs/curriculum/grade12/content/01-sequences-and-series"
    lesson_files = sorted(root.glob("lesson-*.md"))
    assert len(lesson_files) == 18
    for number, path in enumerate(lesson_files, 1):
        source = path.read_text(encoding="utf-8")
        assert f"id: g12-sequences-series-{number:02}" in source
        for heading in ("Learning objective", "Prerequisite diagnostic", "Full concept explanation",
                        "Whiteboard teaching sequence", "Worked examples", "Independent practice",
                        "Complete answers and marking guidance", "Mastery and reteaching rules"):
            assert f"## {heading}" in source


def test_reset_lesson_contract_order_prerequisites_and_mastery():
    batch = lessons()
    assert [lesson.id for lesson in batch] == LESSON_IDS
    assert [lesson.order for lesson in batch] == list(range(1,19))
    assert batch[0].prerequisites == []
    assert batch[1].prerequisites == [LESSON_IDS[0]]
    assert batch[2].prerequisites == [LESSON_IDS[1]]
    assert all(lesson.mastery_threshold == .8 for lesson in batch)
    assert len(batch[0].whiteboard_questions) == 12
    assert all(not lesson.whiteboard_questions for lesson in batch[1:])
    assert batch[0].access_level == AccessLevel.FREE
    assert all(lesson.access_level == AccessLevel.PREMIUM for lesson in batch[1:])


def test_every_lesson_one_example_has_a_valid_deterministic_timeline():
    for question in lessons()[0].whiteboard_questions:
        board = question.whiteboard
        validate_whiteboard(board);validate_visualization(board)
        assert board.visualization.template == "sequence_timeline"
        assert question.answer and question.full_memo and question.misconception_tags
        assert any(event.type == "verify" for step in board.steps for event in step.events)
        for step in board.steps:
            assert step.events == sorted(step.events,key=lambda event:event.at_ms)
            assert step.duration_ms >= step.events[-1].at_ms
            assert " ".join(event.text for event in step.events if event.type=="narration") == " ".join(event.text for event in step.events if event.type=="caption")


def test_arithmetic_and_quadratic_prototypes_calculate_differences_correctly():
    first = lessons()[0].whiteboard_questions
    arithmetic = first[0].whiteboard.visualization.parameters
    geometric = first[1].whiteboard.visualization.parameters
    quadratic = first[2].whiteboard.visualization.parameters
    assert arithmetic["differences"] == [4, 4, 4]
    assert arithmetic["second_differences"] == [0, 0]
    assert first[0].answer == "arithmetic"
    assert quadratic["differences"] == [4, 6, 8]
    assert quadratic["second_differences"] == [2, 2]
    assert first[2].answer == "quadratic"
    assert geometric["ratios"] == ["2", "2", "2"]
    arrow_labels = [event.label for step in first[1].whiteboard.steps for event in step.events if event.type == "draw_arrow"]
    assert arrow_labels == ["×2", "×2", "×2"]
    assert arithmetic["next_term"] == "21"
    assert geometric["next_term"] == "48"
    assert quadratic["next_change"] == "10" and quadratic["next_term"] == "30"


def test_lesson_one_bank_distribution_and_unique_metadata():
    questions=lessons()[0].whiteboard_questions
    assert len({question.id for question in questions})==12
    answers=[question.answer for question in questions]
    assert answers.count("arithmetic")==3
    assert answers.count("geometric")==4  # includes the mixed decreasing classification item
    assert answers.count("quadratic")==5  # includes mixed and error-analysis items
    assert all(question.cognitive_level and question.marks and question.full_memo and question.misconception_tags for question in questions)


def test_timeline_rejects_invalid_order_missing_targets_and_executable_types():
    board = lessons()[0].whiteboard_questions[0].whiteboard
    step = board.steps[0]
    with pytest.raises(ValidationError, match="ordered"):
        step.model_copy(update={"events": [TimelineEvent(at_ms=500,type="pause"), TimelineEvent(at_ms=100,type="pause")]}, deep=True).__class__(**{
            **step.model_dump(), "events":[{"at_ms":500,"type":"pause"},{"at_ms":100,"type":"pause"}]})
    with pytest.raises(ValidationError, match="targets do not exist"):
        board.__class__(**{**board.model_dump(), "steps":[{**step.model_dump(), "events":[{"at_ms":0,"type":"focus","targets":["missing-object"]}]}] + [item.model_dump() for item in board.steps[1:]]})
    with pytest.raises(ValidationError):
        TimelineEvent(at_ms=0, type="execute_javascript")
    with pytest.raises(ValidationError, match="both equation sides"):
        TimelineEvent(at_ms=0, type="apply_both_sides", targets=["left"])
    with pytest.raises(ValidationError, match="earlier matching operation"):
        step.__class__(**{**step.model_dump(), "events":[{"at_ms":0,"type":"cancel","targets":["term-1"]}]})
