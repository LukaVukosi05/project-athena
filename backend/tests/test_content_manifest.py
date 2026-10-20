from fastapi.testclient import TestClient

from app.curriculum.content_manifest import ReadinessState, SOURCE_INVENTORY, manifest_for
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
from app.curriculum.catalogue_compiler import compile_catalogue
from app.main import app


def test_grades_eight_to_twelve_are_registered_from_available_sources():
    grades = curriculum_repository.list_grades()
    assert [grade.id for grade in grades] == [f"grade-{number}" for number in range(8, 13)]
    assert [topic.id for topic in grades[0].topics] == ["algebraic-equations"]
    assert all(not grade.topics for grade in grades[1:4])
    assert len(grades[-1].topics) == 7


def test_manifest_uses_the_six_required_readiness_states_and_stable_ids():
    manifest = manifest_for(curriculum_repository.list_grades())
    assert manifest["states"] == [state.value for state in ReadinessState]
    lessons = [lesson for grade in manifest["grades"] for topic in grade["topics"] for lesson in topic["lessons"]]
    assert len(lessons) == 138
    assert len({lesson["id"] for lesson in lessons}) == 138
    assert {lesson["readiness"] for lesson in lessons} <= set(ReadinessState)
    grade8 = curriculum_repository.get_grade("grade-8")
    released_grade8 = sum(item.release_approved for topic in grade8.topics for subtopic in topic.subtopics for item in subtopic.lessons)
    assert sum(lesson["readiness"] == ReadinessState.PUBLISHED for lesson in lessons) == 6 + released_grade8


def test_missing_master_sources_are_explicit_and_never_reported_as_present():
    missing = [item for item in SOURCE_INVENTORY if not item["present"]]
    assert len(missing) == 3
    assert all(item["lessons_expected"] is None for item in missing)


def test_catalogue_counts_only_usable_runtime_lessons_as_interactive():
    with TestClient(app) as client:
        grade = client.get("/api/v1/curriculum/grades/grade-12").json()
        grade8 = client.get("/api/v1/curriculum/grades/grade-8").json()
        blocked = client.get("/api/v1/curriculum/grades/grade-9").json()
    assert len(grade8["topics"]) == 1
    assert blocked["topics"] == []
    assert all(topic["interactive_lesson_count"] == topic["verified_lesson_count"] + topic["published_interactive_lesson_count"] for topic in grade["topics"])
    counts = {topic["id"]: topic["published_interactive_lesson_count"] for topic in grade["topics"]}
    assert counts["functions-graphs"] == 0
    assert all(value == 1 for topic_id, value in counts.items() if topic_id != "functions-graphs")


def test_aggregate_validator_returns_context_for_every_failure():
    failures = validate_curriculum(curriculum_repository.list_grades())
    for failure in failures:
        assert set(failure.model_dump()) == {"grade_id", "topic_id", "lesson_id", "question_id", "step_id", "failure_reason"}


def test_generated_catalogue_is_deterministic_and_reports_absent_master_sources():
    first, first_discrepancies = compile_catalogue()
    second, second_discrepancies = compile_catalogue()
    assert first == second
    assert first_discrepancies == second_discrepancies
    assert [grade["grade_id"] for grade in first["grades"]] == [f"grade-{number}" for number in range(8, 13)]
    assert len(first["grades"][0]["topics"]) == 1
    assert len(first["grades"][-1]["topics"]) == 7
    assert first_discrepancies == [
        "missing required source: grades-8-9",
        "missing required source: grades-10-11",
        "missing required source: grade-12-requirements",
    ]


def test_grade_list_api_exposes_frontend_catalogue_counts():
    with TestClient(app) as client:
        response = client.get("/api/v1/curriculum/grades")
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 5
    assert all({"topic_count", "expected_lesson_count", "interactive_lesson_count",
                "published_interactive_lesson_count", "availability"} <= set(row) for row in rows)
    assert rows[-1]["topic_count"] == 7
    assert rows[-1]["expected_lesson_count"] == 128


def test_grade8_gold_pack_catalogue_exposes_released_lessons():
    with TestClient(app) as client:
        grade = client.get("/api/v1/curriculum/grades/grade-8")
        topic = client.get("/api/v1/curriculum/grades/grade-8/topics/algebraic-equations")
        lesson = client.get("/api/v1/lessons/g8-algebraic-equations-01")
    assert grade.status_code == 200
    topic_summary = grade.json()["topics"][0]
    assert topic_summary["lesson_count"] == 10
    assert topic_summary["interactive_lesson_count"] == 3
    assert topic_summary["published_interactive_lesson_count"] == 3
    assert topic_summary["availability"] == "available"
    lessons = topic.json()["subtopics"][0]["lessons"]
    assert [item["id"] for item in lessons] == [f"g8-algebraic-equations-{number:02}" for number in range(1, 11)]
    assert lessons[0]["readiness"] == "published" and lessons[0]["usable"]
    assert all(item["readiness"] == "published" and item["usable"] for item in lessons[:3])
    assert all(item["readiness"] == "authored" and not item["usable"] for item in lessons[3:])
    assert all(item["worked_example_count"] == 15 for item in lessons)
    assert all(item["practice_count"] == 15 for item in lessons)
    assert lesson.status_code == 200
    assert lesson.json()["grade_id"] == "grade-8"
