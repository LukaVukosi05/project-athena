from fastapi.testclient import TestClient

from app.curriculum.grade12 import GRADE_12
from app.curriculum.repository import curriculum_repository
from app.curriculum.schemas import AccessLevel
from app.main import app
from app.whiteboard.validation import validate_whiteboard
from app.whiteboard.linear_equations import verify_linear_transition


def test_complete_grade_12_hierarchy_has_unique_ordering():
    assert len(GRADE_12.topics) == 15
    assert [topic.product_order for topic in GRADE_12.topics] == list(range(15))
    assert len({topic.id for topic in GRADE_12.topics}) == 15
    for topic in GRADE_12.topics:
        assert topic.subtopics
        assert [item.order for item in topic.subtopics] == list(range(1, len(topic.subtopics) + 1))
        assert len({item.id for item in topic.subtopics}) == len(topic.subtopics)


def test_readiness_is_not_misrepresented_as_official_caps_topic():
    readiness = GRADE_12.topics[0]
    assert readiness.paper == "Readiness"
    assert readiness.official_caps_topic is None
    assert readiness.term is None


def test_linear_equation_lesson_and_whiteboard_contract():
    result = curriculum_repository.get_lesson("g12-readiness-linear-equations")
    assert result is not None
    _, _, lesson = result
    assert lesson.access_level == AccessLevel.FREE
    assert lesson.prerequisites
    assert lesson.mastery_threshold == 0.8
    whiteboard = next(block for block in lesson.blocks if block.type == "whiteboard")
    validate_whiteboard(whiteboard)
    assert [step.step_number for step in whiteboard.steps] == [0, 1, 2, 3]
    for step in whiteboard.steps:
        assert all([step.explanation.what, step.explanation.why,
                    step.explanation.purpose, step.explanation.remember])
    assert len([block for block in lesson.blocks if block.type == "whiteboard"]) == 1
    assert whiteboard.steps[1].working_expression == "3x + 7 - 7 = 22 - 7"
    assert whiteboard.steps[2].working_expression == "3x / 3 = 15 / 3"
    assert whiteboard.steps[3].working_expression.split("; ") == [
        "3(5) + 7 = 22", "15 + 7 = 22", "22 = 22 ✓"
    ]


def test_curriculum_api_is_lazy_and_lesson_api_returns_blocks():
    with TestClient(app) as client:
        grade = client.get("/api/v1/curriculum/grades/grade-12")
        topic = client.get("/api/v1/curriculum/grades/grade-12/topics/algebra-readiness")
        lesson = client.get("/api/v1/lessons/g12-readiness-linear-equations")
    assert grade.status_code == 200
    assert "subtopics" not in grade.json()["topics"][0]
    assert topic.status_code == 200
    lesson_summaries = [lesson for item in topic.json()["subtopics"] for lesson in item["lessons"]]
    assert lesson_summaries
    assert "blocks" not in lesson_summaries[0]
    assert lesson.status_code == 200
    assert lesson.json()["blocks"]


def test_unknown_resources_return_404():
    with TestClient(app) as client:
        assert client.get("/api/v1/curriculum/grades/grade-7").status_code == 404
        assert client.get("/api/v1/lessons/not-a-lesson").status_code == 404


def test_linear_operations_are_mathematically_equivalent():
    _, _, lesson = curriculum_repository.get_lesson("g12-readiness-linear-equations")
    whiteboard = next(block for block in lesson.blocks if block.type == "whiteboard")
    assert verify_linear_transition(whiteboard.steps[1])
    assert verify_linear_transition(whiteboard.steps[2])
    invalid = whiteboard.steps[1].model_copy(update={"after_expression": "3x = 29"})
    assert not verify_linear_transition(invalid)


def test_free_calculus_lessons_are_detailed_and_exam_framed():
    topic = curriculum_repository.get_topic("grade-12", "differential-calculus")
    lessons = [lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
    assert [lesson.id for lesson in lessons[:2]] == [
        "g12-calculus-average-rate", "g12-calculus-secant-to-tangent"
    ]
    assert all(lesson.access_level == AccessLevel.FREE for lesson in lessons[:2])
    first = lessons[0]
    whiteboard = next(block for block in first.blocks if block.type == "whiteboard")
    assert "EXAM-STYLE QUESTION" in whiteboard.problem
    assert len(whiteboard.steps) == 5
    validate_whiteboard(whiteboard)
    practice = [block for block in first.blocks if block.type == "practice"]
    assert len(practice) == 2
    assert len(practice[1].data["questions"]) == 4
