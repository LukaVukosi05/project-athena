"""Topic 1 must appear as usable, answer-gated Grade 11 course previews."""
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

def test_six_lessons_have_complete_independent_banks_and_valid_steps():
    assert validate_curriculum([GRADE_11]) == []
    lessons = GRADE_11.topics[0].subtopics[0].lessons
    assert len(lessons) == 6
    for number, lesson in enumerate(lessons, 1):
        assert len(lesson.whiteboard_questions) == 15
        assert len(PRACTICE_BANKS[lesson.id]) == 15
        practice, mastery, reassessment, _, _ = BANKS[number]
        assert (len(practice), len(mastery), len(reassessment)) == (15, 5, 3)
        assert len({q.whiteboard.problem for q in lesson.whiteboard_questions}) == 15
        for q in lesson.whiteboard_questions:
            assert len(q.whiteboard.steps) == 5
            assert q.whiteboard.steps[-1].operation.action == "verify_solution"

def test_public_catalogue_and_all_lesson_previews_hide_answers(monkeypatch):
    monkeypatch.setattr("app.api.v1.lessons.enforce_lesson_access", lambda *a: None)
    with TestClient(app) as client:
        grade = client.get("/api/v1/curriculum/grades/grade-11")
        assert grade.status_code == 200
        assert grade.json()["topics"][0]["id"] == "exponents-and-surds"
        for number in range(1, 7):
            lesson = client.get(f"/api/v1/lessons/g11-es-{number:02}")
            assert lesson.status_code == 200
            payload = lesson.json()
            assert len(payload["whiteboard_questions"]) == 15
            for q in payload["whiteboard_questions"]:
                assert q["solution_gated"]
                assert q["total_step_count"] == 5
                assert len(q["whiteboard"]["steps"]) == 1
                assert "answer" not in q and "full_memo" not in q
                assert '"actions"' not in q["whiteboard"]["visualization"]["parameters"]["scene_json"]
            first = payload["whiteboard_questions"][0]["id"]
            revealed = client.post(f"/api/v1/lessons/g11-es-{number:02}/questions/{first}/reveal")
            assert revealed.status_code == 200
            assert len(revealed.json()["whiteboard"]["steps"]) == 5
